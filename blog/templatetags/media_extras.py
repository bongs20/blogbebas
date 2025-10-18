from django import template

register = template.Library()


IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VIDEO_EXTS = {'.mp4', '.webm', '.ogg', '.mov'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a'}


def _lower_ext(name: str) -> str:
    name = (name or '').lower()
    if '.' in name:
        return '.' + name.rsplit('.', 1)[-1]
    return ''


@register.filter
def is_image(name: str) -> bool:
    return _lower_ext(name) in IMAGE_EXTS


@register.filter
def is_video(name: str) -> bool:
    return _lower_ext(name) in VIDEO_EXTS


@register.filter
def is_audio(name: str) -> bool:
    return _lower_ext(name) in AUDIO_EXTS
