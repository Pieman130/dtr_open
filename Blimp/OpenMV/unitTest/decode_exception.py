import sys
import io

def get_exception(err) -> str:
    buf = io.StringIO()
    sys.print_exception(err, buf)
    print(buf.getvalue())
    return buf.getvalue()

try:
    print (1/0)
except Exception as e:
    get_exception(e)
