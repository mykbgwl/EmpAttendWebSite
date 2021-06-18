from MyQR import myqr
import os


def qrgen(s):
    version, level, qr_name = myqr.run(
        str(s),
        level='H',
        version=1,

        # For Background
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(s+'.png'),
        save_dir=os.path.basename("/website")
    )
