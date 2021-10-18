from icon_governance.workers.cron import prep_details_cron_worker


def test_cron_worker(run_process_wait):
    run_process_wait(prep_details_cron_worker)
