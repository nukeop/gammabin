import re
import base64
import uuid


def generate_url():
  rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
  return re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)