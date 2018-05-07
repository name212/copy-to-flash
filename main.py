import platform

from Exceptions import UnsupportedPlatform
from console.ConsoleFactory import ConsoleFactory
from media.MusicFilter import MusicFileFilter
from console.ConsoleArguments import ConsoleArguments
from MusicCopier import MusicCopier
from platforms.PythonDirectory import PythonDirectory


_VERSION = "0.0.1"


def get_available_getter():
    sys = platform.system()
    if sys == "Linux":
        from platforms.LinuxFlashDevice import get_available_devices
        return get_available_devices

    raise UnsupportedPlatform(sys)


if __name__ == "__main__":
    factory = ConsoleFactory()
    controller = factory.get_controller()
    get_available_devices = get_available_getter()
    available_devices = get_available_devices()
    args = ConsoleArguments(
        removable_devices=available_devices,
        controller=controller,
        version_str=_VERSION
    )
    dest = args.get_destination()
    dest = PythonDirectory(dest.get_mount())
    view = factory.get_view()

    def on_delete_print(p):
        if args.is_verbose():
            view.show_deleted(p)

    copier = MusicCopier(
        source_dir=args.get_source(),
        dest_dir=dest,
        filter_obj=MusicFileFilter(),
        on_progress=lambda p, fn, a: view.show_progress(p, fn, a),
        on_delete=on_delete_print
    )

    copier.run()
