from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Course, CourseSchedule, StudentRegistration
from django.contrib import messages
from django.db.models import Q
from .models import Notification

# User sign-up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('thank_you')
        else:
            messages.error(request, "There was an error with your signup. Please check your details and try again.")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Home page
@login_required
def home(request):
    return render(request, 'registration/home.html')

# Logout user
def custom_logout(request):
    logout(request)
    return redirect('user_login')

# Course searching
@login_required
def course_search(request):
    query = request.GET.get('query', '')
    courses = Course.objects.filter(Q(code__icontains=query) | Q(name__icontains=query) | Q(instructor__icontains=query)) if query else Course.objects.none()
    return render(request, 'registration/course_search.html', {'courses': courses, 'query': query})

# Course detail
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    spots_taken = StudentRegistration.objects.filter(course=course).count()
    available_spots = course.capacity - spots_taken
    context = {'course': course, 'available_spots': available_spots}
    return render(request, 'registration/course_detail.html', context)

# Course schedule
def course_schedule(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    try:
        schedule = CourseSchedule.objects.get(course=course)
    except CourseSchedule.DoesNotExist:
        messages.error(request, "No schedule available for this course.")
        return redirect('course_detail', course_id=course_id)
    
    context = {
        'course': course,
        'schedule': schedule,
        'available_spots': course.capacity - StudentRegistration.objects.filter(course=course).count()
    }
    return render(request, 'registration/course_schedule.html', context)

# Register course
@login_required
def register_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    student = request.user.student  # Make sure the student object is properly linked with User

    if request.method == 'POST':
        # Check if the course is already registered
        if StudentRegistration.objects.filter(student=student, course=course).exists():
            messages.error(request, "You are already registered for this course.")
        else:
            # Check for available spots
            if course.available_spots > 0:
                StudentRegistration.objects.create(student=student, course=course)
                course.available_spots -= 1  # Decrement the spot
                course.save()
                messages.success(request, "Successfully registered for the course.")
                return redirect('view_schedule')
            else:
                messages.error(request, "No available spots for this course.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('course_detail', course_id=course_id)

@login_required
def view_schedule(request):
    student = request.user.student
    registrations = StudentRegistration.objects.filter(student=student).select_related('course', 'course__courseschedule')

    # Here, we assume each course must have a linked courseschedule. Adjust logic as needed.
    courses_with_schedules = [{
        'course': registration.course,
        'schedule': registration.course.courseschedule
    } for registration in registrations if hasattr(registration.course, 'courseschedule')]

    return render(request, 'registration/view_schedule.html', {
        'courses_with_schedules': courses_with_schedules
    })

def thank_you(request):
    return render(request, 'thank_you.html')


from django.db.models import Count
from .models import Course, StudentRegistration

def course_popularity_report(request):
    course_data = Course.objects.annotate(registrations_count=Count('studentregistration'))
    labels = [course.name for course in course_data]
    data = [course.registrations_count for course in course_data]
    return render(request, 'reports/course_popularity.html', {'labels': labels, 'data': data})


def available_courses(request):
    student = request.user.student
    completed_courses = student.completed_courses.all()
    available_courses = Course.objects.filter(
        prerequisites__in=completed_courses
    ).distinct()
    return render(request, 'courses/available_courses.html', {'courses': available_courses})


def home(request):
    notifications = Notification.objects.filter(active=True).order_by('-date_created')
    return render(request, 'home.html', {'notifications': notifications})