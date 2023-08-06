from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from opennem.api.time import human_to_interval, human_to_period
from opennem.core.networks import network_from_network_code
from opennem.core.normalizers import normalize_duid
from opennem.core.units import get_unit
from opennem.db import get_database_engine, get_database_session
from opennem.db.models.opennem import Facility, Station
from opennem.utils.time import human_to_timedelta
from opennem.utils.timezone import make_aware

from .controllers import stats_factory
from .queries import (
    energy_facility,
    energy_network,
    power_facility,
    price_network_region,
)
from .schema import (
    DataQueryResult,
    OpennemData,
    OpennemDataHistory,
    OpennemDataSet,
)

router = APIRouter()


@router.get(
    "/power/unit/{network_code}/{unit_code:path}",
    name="stats:Unit Power",
    response_model=OpennemData,
)
def power_unit(
    unit_code: str = Query(..., description="Unit code"),
    network_code: str = Query(..., description="Network code"),
    since: str = Query(None, description="Since as human interval"),
    since_dt: datetime = Query(None, description="Since as datetime"),
    interval: str = Query(None, description="Interval"),
    period: str = Query("7d", description="Period"),
    session: Session = Depends(get_database_session),
    engine=Depends(get_database_engine),
) -> OpennemData:
    if not since:
        since = datetime.now() - human_to_timedelta("7d")

    network = network_from_network_code(network_code)

    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such network",
        )

    if not interval:
        interval = "{}m".format(network.interval_size)

    interval = human_to_interval(interval)
    period = human_to_period(period)
    units = get_unit("power")

    stats = []

    facility_codes = [normalize_duid(unit_code)]

    query = power_facility(
        facility_codes, network.code, interval=interval, period=period
    )

    with engine.connect() as c:
        results = list(c.execute(query))

    stats = [
        DataQueryResult(
            interval=i[0], result=i[1], group_by=i[2] if len(i) > 1 else None
        )
        for i in results
    ]

    if len(stats) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unit stats not found",
        )

    output = stats_factory(
        stats,
        code=unit_code,
        interval=interval,
        period=period,
        units=units,
        network=network,
    )

    return output


@router.get(
    "/power/station/{network_code}/{station_code:path}",
    name="stats:Station Power",
    response_model=OpennemDataSet,
)
def power_station(
    station_code: str = Query(..., description="Station code"),
    network_code: str = Query(..., description="Network code"),
    since: datetime = Query(None, description="Since time"),
    interval: str = Query(None, description="Interval"),
    period: str = Query("7d", description="Period"),
    session: Session = Depends(get_database_session),
    engine=Depends(get_database_engine),
) -> OpennemDataSet:
    if not since:
        since = datetime.now() - human_to_timedelta("7d")

    network = network_from_network_code(network_code)

    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such network",
        )

    if not interval:
        # @NOTE rooftop data is 15m
        if station_code.startswith("ROOFTOP"):
            interval = "15m"
        else:
            interval = "{}m".format(network.interval_size)

    interval = human_to_interval(interval)
    period = human_to_period(period)
    units = get_unit("power")

    station = (
        session.query(Station)
        .join(Facility)
        .filter(Station.code == station_code)
        .filter(Facility.network_id == network.code)
        .filter(Station.approved == True)
        .one_or_none()
    )

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Station not found"
        )

    facility_codes = list(set([f.code for f in station.facilities]))

    stats = []

    query = power_facility(
        facility_codes, network_code, interval=interval, period=period
    )

    # print(query)

    with engine.connect() as c:
        results = list(c.execute(query))

    stats = [
        DataQueryResult(
            interval=i[0], result=i[1], group_by=i[2] if len(i) > 1 else None
        )
        for i in results
    ]

    if len(stats) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station stats not found",
        )

    result = stats_factory(
        stats,
        code=station_code,
        network=network,
        interval=interval,
        period=period,
        units=units,
    )

    return result


@router.get(
    "/energy/station/{network_code}/{station_code}",
    name="Energy Station",
    response_model=OpennemDataSet,
)
def energy_station(
    engine=Depends(get_database_engine),
    session: Session = Depends(get_database_session),
    network_code: str = Query(..., description="Network code"),
    station_code: str = Query(..., description="Station Code"),
    interval: str = Query(None, description="Interval"),
    period: str = Query("7d", description="Period"),
) -> OpennemDataSet:
    """
        Get energy output for a station (list of facilities)
        over a period
    """

    network = network_from_network_code(network_code)

    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such network",
        )

    if not interval:
        # @NOTE rooftop data is 15m
        if station_code.startswith("ROOFTOP"):
            interval = "15m"
        else:
            interval = "{}m".format(network.interval_size)

    interval = human_to_interval(interval)
    period = human_to_period(period)
    units = get_unit("energy")

    station = (
        session.query(Station)
        .join(Station.facilities)
        .filter(Station.code == station_code)
        .filter(Facility.network_id == network.code)
        .one_or_none()
    )

    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Station not found"
        )

    if len(station.facilities) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station has no facilities",
        )

    facility_codes = list(set([f.code for f in station.facilities]))

    query = energy_facility(
        facility_codes, network_code, interval=interval, period=period
    )

    with engine.connect() as c:
        results = list(c.execute(query))

    stats = [
        DataQueryResult(
            interval=i[0], result=i[1], group_by=i[2] if len(i) > 1 else None
        )
        for i in results
    ]

    if len(stats) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station stats not found",
        )

    result = stats_factory(
        stats,
        code=station_code,
        network=network,
        interval=interval,
        period=period,
        units=units,
    )

    return result


@router.get(
    "/energy/network/{network_code}",
    name="Energy Network",
    response_model=OpennemDataSet,
)
def energy_network_api(
    engine=Depends(get_database_engine),
    network_code: str = Query(..., description="Network code"),
    interval: str = Query("1d", description="Interval"),
    period: str = Query("1Y", description="Period"),
) -> OpennemDataSet:

    results = []

    network = network_from_network_code(network_code)

    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such network",
        )

    if not interval:
        interval = "{}m".format(network.interval_size)

    interval = human_to_interval(interval)
    period = human_to_period(period)
    units = get_unit("energy")

    query = energy_network(network=network, interval=interval, period=period)

    with engine.connect() as c:
        results = list(c.execute(query))

    if len(results) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No results"
        )

    stats = [
        DataQueryResult(
            interval=i[0], result=i[1], group_by=i[2] if len(i) > 1 else None
        )
        for i in results
    ]

    result = stats_factory(
        stats,
        code=network.code,
        network=network,
        interval=interval,
        period=period,
        units=units,
    )

    return result


@router.get(
    "/price/{network_code}/{region_code}",
    name="Price Network Region",
    response_model=OpennemDataSet,
)
def price_network_region_api(
    engine=Depends(get_database_engine),
    network_code: str = Query(..., description="Network code"),
    region_code: str = Query(..., description="Region code"),
    interval: str = Query(None, description="Interval"),
    period: str = Query("7d", description="Period"),
) -> OpennemDataSet:
    network = network_from_network_code(network_code)

    if not network:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such network",
        )

    if not interval:
        interval = "{}m".format(network.interval_size)

    interval = human_to_interval(interval)
    period = human_to_period(period)
    units = get_unit("price")

    query = price_network_region(
        network=network,
        region_code=region_code,
        interval=interval,
        period=period,
    )

    with engine.connect() as c:
        results = list(c.execute(query))

    if len(results) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No data found"
        )

    stats = [
        DataQueryResult(
            interval=i[0], result=i[1], group_by=i[2] if len(i) > 1 else None
        )
        for i in results
    ]

    result = stats_factory(
        stats,
        code=network.code,
        region=region_code,
        network=network,
        interval=interval,
        period=period,
        units=units,
    )

    return result
