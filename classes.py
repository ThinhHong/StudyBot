class StudyTime:
    '''Class for keeping track of study time.'''
    is_studying: bool
    max_time: int
    break_time = int

    def __init__(
            self, 
            is_studying = False,
            max_time = 45,
            break_time = 15
          
        ) -> None:
        self.is_studying=is_studying
        self.max_time=max_time
        self.break_time = break_time
      

    def __repr__(self) -> str:
        return (
            'Study session('
            f'is studying:{self.is_studying!r}, max_timeL{self.max_time!r}, '
            f'break_time:{self.break_time!r})'
        )

    def __hash__(self) -> int:
        return hash((self.is_studying, self.max_time, self.break_time))


