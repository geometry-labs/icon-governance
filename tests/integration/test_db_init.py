from icon_governance.db import session
from icon_governance.db_init import get_initial_preps
from icon_governance.models.preps import Prep

# def test_get_initial_preps(run_process_wait):
#     run_process_wait(get_initial_preps)
#     prep = session.get(Prep, "hx9121c5914ce34f59de52fe15efd6f7982c2ab8ae")
#     assert prep
