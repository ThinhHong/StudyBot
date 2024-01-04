class StudyTime:
    '''Class for keeping track of study time.'''
    is_studying: bool
    start_time: int

    def __init__(
            self, 
            is_studying = False,
            start_time = 0
        ) -> None:
        self.is_studying=is_studying
        self.start_time=start_time

    def time_studied(self) -> float:
        return self.is_studying
    
    