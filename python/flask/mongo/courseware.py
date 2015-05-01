from app import db

from models import Courseware


def get_course_courseware_list(user):
    courses = user.courses[:]
    course_ids = [c.id for c in courses]
    query = {
        'course': {'$in': course_ids},
        'state': Courseware.STATE_CONVERTED if user.is_teacher else Courseware.STATE_FINISHED
    }
    coursewares = db.Courseware.find(query)
    course_dict = organize_courses(courses, coursewares)
    find_newwares(user, coursewares, course_dict)


def organize_courses(courses, coursewares):
    course_dict = {}
    for c in courses:
        course_dict[c.id] = c
        c.coursewares = {}
        c.newwares = {}
    for courseware in coursewares:
        category = courseware.category.id
        course = course_dict[courseware.course.id]
        lst = course.coursewares.setdefault(category, [])
        lst.append(courseware)
        course.newwares.setdefault(category, 0)
    return course_dict
    

def find_newwares(user, coursewares, course_dict=None):
    newware_set = set(user.newwares)
    for courseware in coursewares:
        if courseware.id in newware_set:
            courseware.new = True
            courseware.downloaded = False
            if course_dict:
                course = course_dict[courseware.course.id]
                course.newwares[courseware.category.id] += 1
        else:
            courseware.new = False
            courseware.downloaded = True
            

def get_delivered(user, courseware_id):
    delivered = db.Delivered.one({'courseware': courseware_id, 'device': user.device})
    if not delivered:
        courseware = db.Courseware.one({'_id': courseware_id})
        delivered = local_deliver(user, courseware_id, courseware.outpath)
    if delivered:
        if _file_exists(delivered.outpath) and \
           os.path.getmtime(delivered.outpath) > os.path.getmtime(delivered.srcpath) \
           or local_deliver(user, courseware_id, delivered.srcpath, delivered.outpath):
            return delivered
    return None
    
    
def local_deliver(user, courseware_id, srcpath, outpath=None):
    pass
    