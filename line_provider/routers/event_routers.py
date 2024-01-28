from fastapi import APIRouter, status, HTTPException
from models import Event
from schemas import (
    UnavailableService,
    event_pydantic_model,
    EventNotFound,
    EventChangeSuccess,
    StatusNotFound,
    EventCreate
)


event_router = APIRouter(prefix="", tags=["event"])


@event_router.get(
    "/events",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": UnavailableService}},
)
async def get_events():
    return await event_pydantic_model.from_queryset(Event.all())


@event_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"message": "Event has been created successfully"},
        status.HTTP_400_BAD_REQUEST: {"message": "Bad request"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": UnavailableService},
    },
)
async def create_event(event: EventCreate):
    event_object = await Event.create(**event.dict())
    return await event_pydantic_model.from_tortoise_orm(event_object)


@event_router.get(
    "/event/{uuid}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"message": "Bad request"},
        status.HTTP_404_NOT_FOUND: {"message": "Event not found"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": UnavailableService},
    },
)
async def get_event(uuid: str):
    return await event_pydantic_model.from_queryset_single(Event.get(uuid=uuid))


@event_router.patch(
    "/change_ratio/{uuid}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": EventNotFound},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": UnavailableService},
    },
)
async def change_ratio(uuid: str, ratio: float):
    event = await Event.get_or_none(uuid=uuid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EventNotFound(message="Event not found", uuid=uuid),
        )
    event.ratio = ratio
    await event.save()
    return await event


@event_router.delete(
    "/delete/{uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"message": "Event has been deleted successfully"},
        status.HTTP_404_NOT_FOUND: {"message": "Event not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": UnavailableService},
    },
)
async def delete_event(uuid: str):
    await Event.filter(uuid=uuid).delete()
    return status.HTTP_204_NO_CONTENT


@event_router.get(
    "/get_status",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": StatusNotFound},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": UnavailableService},
    },
)
async def event_get_status(event_uuid: str):
    event = await event_pydantic_model.from_queryset_single(
        Event.get_or_none(uuid=event_uuid)
    )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EventNotFound(message="Event not found", uuid=event_uuid),
        )
    return event.status


@event_router.put(
    "/change_status",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": EventChangeSuccess},
        status.HTTP_404_NOT_FOUND: {"model": StatusNotFound},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": UnavailableService},
    },
)
async def event_change_status(event_uuid: str, new_status: int):
    event = await Event.get_or_none(uuid=event_uuid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EventNotFound(message="Event not found", uuid=event_uuid),
        )
    event.status = new_status
    await event.save()
    return EventChangeSuccess(message="Status has been changed", status=new_status)
