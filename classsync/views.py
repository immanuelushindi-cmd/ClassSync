import subprocess, sys

try:
    import qrcode
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'qrcode[pil]'])
    import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Session, Doubt, Vote, StudentPresence
import uuid


def home(request):
    return render(request, 'classsync/home.html')


def create_session(request):
    if request.method == 'POST':
        title        = request.POST.get('title', '').strip()
        subject      = request.POST.get('subject', '').strip()
        teacher_name = request.POST.get('teacher_name', '').strip()
        if title and subject and teacher_name:
            session = Session.objects.create(title=title, subject=subject, teacher_name=teacher_name)
            owned = request.session.get('owned_sessions', [])
            owned.append(session.pin)
            request.session['owned_sessions'] = owned
            return redirect('teacher_dashboard', pin=session.pin)
    return render(request, 'classsync/create_session.html')


def teacher_dashboard(request, pin):
    session  = get_object_or_404(Session, pin=pin)
    doubts   = session.doubts.filter(is_answered=False)
    answered = session.doubts.filter(is_answered=True)
    return render(request, 'classsync/teacher_dashboard.html', {
        'session': session, 'doubts': doubts, 'answered': answered,
    })


@require_POST
def end_session(request, pin):
    session = get_object_or_404(Session, pin=pin)
    session.is_active = False
    session.save()
    return redirect('session_analytics', pin=pin)


def join_session(request):
    error = None
    if request.method == 'POST':
        pin = request.POST.get('pin', '').strip()
        try:
            session = Session.objects.get(pin=pin, is_active=True)
            return redirect('student_room', pin=session.pin)
        except Session.DoesNotExist:
            error = 'Invalid PIN or session has ended. Please check with your teacher.'
    return render(request, 'classsync/join.html', {'error': error})


def student_room(request, pin):
    session = get_object_or_404(Session, pin=pin, is_active=True)
    if not request.session.get('voter_key'):
        request.session['voter_key'] = str(uuid.uuid4())
    doubts = session.doubts.filter(is_answered=False)
    return render(request, 'classsync/student_room.html', {'session': session, 'doubts': doubts})


@require_POST
def submit_doubt(request, pin):
    session   = get_object_or_404(Session, pin=pin, is_active=True)
    text      = request.POST.get('text', '').strip()
    topic_tag = request.POST.get('topic_tag', '').strip().lower().replace('#', '')
    if not text:
        return JsonResponse({'status': 'error', 'message': 'Empty doubt'}, status=400)
    doubt = Doubt.objects.create(session=session, text=text, topic_tag=topic_tag)
    return JsonResponse({'status': 'ok', 'doubt_id': doubt.id, 'text': doubt.text,
                         'topic_tag': doubt.topic_tag, 'votes': doubt.votes})


@require_POST
def upvote_doubt(request, doubt_id):
    doubt     = get_object_or_404(Doubt, id=doubt_id)
    voter_key = request.session.get('voter_key')
    if not voter_key:
        voter_key = str(uuid.uuid4())
        request.session['voter_key'] = voter_key
    _, created = Vote.objects.get_or_create(doubt=doubt, voter_key=voter_key)
    if created:
        doubt.votes += 1
        doubt.save()
    return JsonResponse({'votes': doubt.votes, 'already_voted': not created})


@require_POST
def mark_answered(request, doubt_id):
    doubt = get_object_or_404(Doubt, id=doubt_id)
    doubt.is_answered = True
    doubt.save()
    return JsonResponse({'status': 'answered', 'doubt_id': doubt.id})


@require_POST
def presence_ping(request, pin):
    session   = get_object_or_404(Session, pin=pin, is_active=True)
    voter_key = request.session.get('voter_key')
    if not voter_key:
        voter_key = str(uuid.uuid4())
        request.session['voter_key'] = voter_key
    StudentPresence.objects.update_or_create(session=session, voter_key=voter_key)
    return JsonResponse({'status': 'ok', 'online': session.online_count()})


def live_doubts_api(request, pin):
    session     = get_object_or_404(Session, pin=pin)
    open_doubts = session.doubts.filter(is_answered=False).values(
        'id', 'text', 'votes', 'topic_tag'
    ).order_by('-votes', '-submitted_at')
    return JsonResponse({
        'doubts':          list(open_doubts),
        'confusion_score': session.confusion_score(),
        'open_count':      session.open_count(),
        'total_doubts':    session.doubts.count(),
        'answered_count':  session.answered_count(),
        'online_count':    session.online_count(),
    })


def session_history(request):
    sessions = Session.objects.all().order_by('-created_at')
    return render(request, 'classsync/history.html', {'sessions': sessions})


def session_analytics(request, pin):
    session    = get_object_or_404(Session, pin=pin)
    tag_data   = list(session.doubts.exclude(topic_tag='').values('topic_tag')
                      .annotate(count=Count('id')).order_by('-count'))
    top_doubts = session.doubts.order_by('-votes')[:5]
    return render(request, 'classsync/analytics.html', {
        'session': session, 'tag_data': tag_data, 'top_doubts': top_doubts,
    })


def session_qr(request, pin):
    import qrcode, io, socket
    from django.http import HttpResponse

    session = get_object_or_404(Session, pin=pin)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = '127.0.0.1'

    port = request.get_port()
    join_url = f'http://{local_ip}:{port}/session/{pin}/student/'

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(join_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')
