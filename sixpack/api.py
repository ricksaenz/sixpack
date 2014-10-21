from models import Experiment, Alternative, Client
from config import CONFIG as cfg
import sys


def participate(experiment, alternatives, client_id,
    force=None,
    traffic_fraction=None,
    alternative=None,
    datetime=None,
    redis=None,
    override=None):

    exp = Experiment.find_or_create(experiment, alternatives, traffic_fraction=traffic_fraction, redis=redis)
    print >> sys.stderr, 'participate'
    sys.stderr.flush()
    alt = None
    if force and force in alternatives:
        alt = Alternative(force, exp, redis=redis)
    elif not cfg.get('enabled', True):
        alt = exp.control
    elif exp.winner is not None:
        alt = exp.winner
    elif override and override in alternatives:
        client = Client(client_id, redis=redis)
        alt = exp.set_alternative(client, alternative=override, dt=datetime)
    else:
        client = Client(client_id, redis=redis)
        alt = exp.get_alternative(client, alternative=alternative, dt=datetime)

    return alt


def convert(experiment, client_id,
    kpi=None,
    datetime=None,
    redis=None):

    exp = Experiment.find(experiment, redis=redis)

    if cfg.get('enabled', True):
        client = Client(client_id, redis=redis)
        alt = exp.convert(client, dt=datetime, kpi=kpi)
    else:
        alt = exp.control

    return alt
