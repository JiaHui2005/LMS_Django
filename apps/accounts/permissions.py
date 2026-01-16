def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_lecturer(user):
    return user.is_authenticated and user.role == 'lecturer'

def is_coordinator(user):
    return user.is_authenticated and user.role == 'coordinator'

def is_cs(user):
    return user.is_authenticated and user.role == 'cs'

def is_student(user):
    return user.is_authenticated and user.role == 'student'

    