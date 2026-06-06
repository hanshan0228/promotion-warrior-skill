import argparse
import json
import subprocess
import shutil
from pathlib import Path

from lib.transcript_io import write_json


def resolve_ffmpeg_path() -> str | None:
    return shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch YouTube metadata and media assets.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--download-video", action="store_true")
    parser.add_argument("--download-audio", action="store_true")
    parser.add_argument("--metadata-output", required=True)
    return parser.parse_args()


def run_command(cmd: list[str]) -> tuple[bool, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout
    return False, (result.stderr or result.stdout or "").strip()


def fetch_metadata(url: str) -> dict:
    ok, output = run_command(["yt-dlp", "--cookies-from-browser", "chrome", "--remote-components", "ejs:github", "--dump-single-json", "--no-playlist", url])
    if not ok:
        raise RuntimeError(f"yt-dlp metadata fetch failed: {output}")
    raw = json.loads(output)
    subtitles = raw.get("subtitles") or {}
    auto_captions = raw.get("automatic_captions") or {}
    return {
        "version": "1.0",
        "video": {
            "id": raw.get("id", "unknown"),
            "title": raw.get("title", "Unknown Title"),
            "duration_sec": float(raw.get("duration") or 0.0),
            "webpage_url": raw.get("webpage_url", url),
        },
        "download": {
            "video_path": "source/video.mp4",
            "audio_path": "source/audio.mp3",
        },
        "subtitles": {
            "manual_languages": sorted(subtitles.keys()),
            "auto_languages": sorted(auto_captions.keys()),
        },
    }


def download_video(url: str, output_dir: str) -> None:
    ok, output = run_command(["yt-dlp", "--cookies-from-browser", "chrome", "--remote-components", "ejs:github", "-f", "mp4/bestvideo+bestaudio/best", "-o", str(Path(output_dir) / "video.mp4"), url])
    if not ok:
        raise RuntimeError(f"yt-dlp video download failed: {output}")


def download_audio(url: str, output_dir: str) -> None:
    cmd = ["yt-dlp", "--cookies-from-browser", "chrome", "--remote-components", "ejs:github", "-x", "--audio-format", "mp3", "-o", str(Path(output_dir) / "audio.%(ext)s")]
    ffmpeg_path = resolve_ffmpeg_path()
    if ffmpeg_path:
        cmd.extend(["--ffmpeg-location", ffmpeg_path])
    cmd.append(url)
    ok, output = run_command(cmd)
    if not ok:
        raise RuntimeError(f"yt-dlp audio download failed: {output}")


def main() -> None:
    args = parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    metadata = fetch_metadata(args.url)
    if args.download_video:
        download_video(args.url, args.output_dir)
    if args.download_audio:
        download_audio(args.url, args.output_dir)
    write_json(args.metadata_output, metadata)


if __name__ == "__main__":
    main()
