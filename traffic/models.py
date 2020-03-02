# coding: utf-8
from django.db import models


STATE_RED = "stop"
STATE_YELLOW = "caution"
STATE_GREEN = "gogogo"

STATE_CHOICES = (
    (STATE_RED, STATE_RED),
    (STATE_YELLOW, STATE_YELLOW),
    (STATE_GREEN, STATE_GREEN),
)

TRANSITIONS = {
    STATE_RED: STATE_GREEN,
    STATE_YELLOW: STATE_RED,
    STATE_GREEN: STATE_YELLOW,
}


class TrafficLight(models.Model):
    """to change state of the traffic light call `TrafficLight().transition()`
    """

    # keep state when initalising the model to avoid additional DB lookups
    __current_state = None

    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default=STATE_RED
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_state = self.state

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        allowed_next = TRANSITIONS[self.__current_state]

        # skip validation if the model is being created
        updated = self.state != self.__current_state
        if self.pk and updated and allowed_next != self.state:
            raise Exception("Invalid transition.", self.state, allowed_next)

        # manually set __current_state to ensure instances can be used mutliple
        # times without running into validation errors
        if self.pk and updated:
            self.__current_state = allowed_next

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def transition(self):
        next_state = TRANSITIONS[self.state]
        self.state = next_state
        self.save()
