from dishka import provide_all, Provider, Scope

from telegram_bot_sample.application.interactors.user.check_user_is_owner import \
    CheckUserIsOwnerInteractor


class InteractorProvider(Provider):
    scope = Scope.REQUEST
    
    provides = provide_all(
        CheckUserIsOwnerInteractor,
    )
