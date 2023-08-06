import logging
from datetime import datetime
from pprint import pprint

from sqlalchemy.orm.session import make_transient

from opennem.core.loader import load_data
from opennem.db import engine, session
from opennem.db.initdb import init_opennem
from opennem.db.load_fixtures import load_fixtures
from opennem.db.models.opennem import Facility, Location, Revisions, Station
from opennem.importer.mms import mms_import
from opennem.importer.registry import registry_import
from opennem.schema.opennem import StationSchema

logger = logging.getLogger(__name__)


def load_revisions(stations):
    pass


def create_revision(model):
    # s = session()

    # make_transient(model)

    clone = model.asdict(exclude_pk=True)
    # clone.pop("id")
    # model.fromdict(clone)
    clone_model = Station().fromdict(clone)

    return clone_model


def db_test():
    logger.info("Running db test")
    registry = registry_import()

    s = session()

    all_stations = [i.code for i in s.query(Station.code).distinct()]
    all_facilities = [i.code for i in s.query(Facility.code).distinct()]

    for station in registry:
        station_dict = station.dict(exclude={"id"})
        # pprint(station_dict)

        station_model = Station().fromdict(station_dict)
        station_model.approved = True
        station_model.approved_at = datetime.now()
        station_model.approved_by = "opennem.registry"
        station_model.created_by = "opennem.registry"

        for fac in station.facilities:
            f = Facility(
                **fac.dict(exclude={"id", "fueltech", "status", "network"})
            )

            f.network_id = fac.network.code

            if fac.fueltech:
                f.fueltech_id = fac.fueltech.code

            f.status_id = fac.status.code

            station_model.facilities.append(f)

        s.add(station_model)

    s.commit()

    # ....

    mms = mms_import()

    for station_record in mms:
        station_model = (
            s.query(Station)
            .filter(Station.code == station_record.code)
            .one_or_none()
        )

        if not station_model:
            logger.info(
                f"New station {station_record.name} {station_record.code}"
            )

            station_dict = station_record.dict(exclude={"id"})

            station_model = Station().fromdict(station_dict)
            station_model.approved = True
            station_model.approved_at = datetime.now()
            station_model.approved_by = "opennem.mms"
            station_model.created_by = "opennem.mms"

            for fac in station_record.facilities:
                f = Facility(
                    **fac.dict(exclude={"id", "fueltech", "status", "network"})
                )

                f.network_id = fac.network.code

                if fac.fueltech:
                    f.fueltech_id = fac.fueltech.code

                f.status_id = fac.status.code

                station_model.facilities.append(f)

            s.add(station_model)


def test_revisions():
    registry = registry_import()
    # mms = mms_import()
    s = session()

    k = registry.get_code("KWINANA")

    station = Station(code=k.code, name=k.name, network_name=k.network_name,)
    s.add(station)
    s.commit()

    station_clone = station.asdict()
    station_clone.pop("id")

    pprint(station_clone)

    station = create_revision(station)

    station.location = Location(
        address1=k.location.address1,
        address2=k.location.address2,
        locality=k.location.locality,
        state=k.location.state,
        postcode=k.location.postcode,
    )

    s.add(station)
    s.commit()

    station = create_revision(station)

    station.name = "Kwinana Edited"

    s.add(station)
    s.commit()


if __name__ == "__main__":
    init_opennem(engine)
    # logger.info("Db initialized")

    load_fixtures()
    # logger.info("Fixtures loaded")

    db_test()
