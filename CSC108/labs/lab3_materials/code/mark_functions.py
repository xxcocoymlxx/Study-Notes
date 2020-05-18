def percentage(raw_mark, max_mark):
    ''' (float, float) -> float
    Return the percentage mark on a piece of work that received a mark of
    raw_mark where the maximum possible mark is max_mark.
    >>> percentage(15, 20)
    75.0
    '''
    return ((raw_mark / max_mark) * 100)

def contribution(mark_as_percent, weight):
    ''' (float, float) -> float
    Given a piece of work that earned mark_as_percent percent and was
    worth weight marks in the marking scheme, return the number of marks it
    contributes to the final course mark.
    >>> contribution(50, 12.5)
    6.25
    '''
    return (weight * (mark_as_percent / 100))

def raw_contribution(raw_mark, max_mark, weight):
    ''' (float, float, float) -> float
    Given a piece of work where the student earned raw_mark marks out of a
    maximum of max_marks marks possible, return the number of marks it
    contributes to the final course mark if this piece of work is worth weight
    marks in the course marking scheme.
    >>> raw_contribution(13.5, 15, 10)
    9.0
    '''
    return (percentage(raw_mark, max_mark) * weight / 100)

def assignments_contribution(a1, a2, a3):
    '''
    Given raw marks a1, a2 and a3 for the three course assignments,
    calculate the contribution to the final course grade.
    Assume each assignment is marked out of 50.
    The assignments are worth 10%, 15%, and 15%, respectively.
    >>> assignments_contribution(40, 42, 40)
    32.6
    '''
    return ((a1 / 50 * 10) + (a2 / 50 * 15) + (a3 / 50 * 15))

def term_work_mark(assignments, quizzes_and_exercises, labs, midterm):
    '''(float, float, float, float, float) -> float
    Given the contribution of:
      assignments (out of 40)
      quizzes and mini-exercises (out of 5)
      labs (out of 10)
      and midterm (as a percentage out of 100),
      return the term mark grade.
      The midterm is worth 10%, so
        the returned mark represents a mark out of 65.
    >>> term_work_mark(28, 4.5, 7, 73.5)
    46.85
    '''
    assignments = assignments_contribution(a1, a2, a3)
    quizes_and_ecercises =
    labs = labs * 10
    midterm = 
    return 

def exam_required(term_work, desired_grade):
    ''' (float, int) -> float
    Given a term work mark of term_work representing 65% of the points in the
    grading scheme, calculate and return the percentage required on the exam for
    the final mark to be desired_grade.
    >>> exam_required(54, 82)
    80.0
    '''
