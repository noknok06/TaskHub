STATUS_UNPROCESSED = 10
STATUS_HOLD = 20
STATUS_INWORK = 30
STATUS_OUTWORK = 40
STATUS_FINISH = 50

STATUS_CHOICES = [
    (STATUS_UNPROCESSED, '未処理'),
    (STATUS_HOLD, '保留'),
    (STATUS_INWORK, '社内確認中'),
    (STATUS_OUTWORK, 'ベンダー作業中'),
    (STATUS_FINISH, '完了'),
]