from Library.Services.Generic.GenericZoom import GenericZoomService
from Library.Services.Generic.GenericHangouts import GenericHangoutsService
from Library.Services.Generic.GenericTeams import GenericTeamsService


def main():
    #Define your feeds
    feeds = [GenericZoomService(output="/var/lib/seethru/Generic/outputs/zoomService.json"),
            GenericHangoutsService(output="/var/lib/seethru/Generic/outputs/hangoutsService.json"),
            GenericTeamsService(output="/var/lib/seethru/Generic/outputs/teamsService.json")]

    # Runs your feeds
    for feed in feeds:
        feed.run()
        feed.export()

if __name__ == "__main__":
    main()
