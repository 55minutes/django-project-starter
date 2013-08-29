from fabric.colors import green


def notify_ok(msg):
    print(green(msg))


def created(msg):
    notify_ok('Created {}'.format(msg))


def generated(msg):
    notify_ok('Generated {}'.format(msg))
