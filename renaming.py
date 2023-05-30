import os
import argparse
import re

MEDIA_FOLDER = "/run/user/1000/gvfs/smb-share:server=192.168.253.115,share=media"

parser = argparse.ArgumentParser()
parser.add_argument("path")

parser.add_argument("-n", "--name", type=str, required=True)
parser.add_argument("-s", "--season", type=str, required=True)

args = parser.parse_args()

target_dir = os.path.join(MEDIA_FOLDER, args.path)


class Episode:
    def __init__(
        self, episode_name: str, episode_name_tvdb: str, season_number: str
    ) -> None:
        self.episode_name = episode_name
        self.episode_number = re.findall(r"E(\d+)\s", self.episode_name)[0]
        self.episode_name_tvdb = episode_name_tvdb
        self.season_number = season_number

    def get_episode(self):
        return (
            f"{self.episode_name_tvdb} - {self.season_number}x{self.episode_number}.mkv"
        )

    def get_folder_name(self):
        return f"{self.episode_name}"

    def __str__(self) -> str:
        print(f"{self.episode_name}")


if __name__ == "__main__":
    # path exists ?
    if not os.path.exists(target_dir):
        print(f"{target_dir} does not exist")
        exit(1)

    # grabbing episodes name
    episodes_obj = []
    episodes_data = os.listdir(target_dir)

    for episode in episodes_data:
        episodes_obj.append(Episode(episode, args.name, args.season))

    for episode in episodes_obj:
        if os.path.exists(os.path.join(target_dir, episode.get_folder_name())):
            os.rename(
                os.path.join(target_dir, episode.get_folder_name()),
                os.path.join(target_dir, episode.get_episode()),
            )
