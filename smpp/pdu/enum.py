def old_style_enum(*sequential, **named):
    enums = dict(zip(sequential, sequential), **named)
    return type('Enum', (), enums)
