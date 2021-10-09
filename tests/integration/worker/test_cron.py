from icon_governance.workers.cron import cron_worker


def test_cron_worker(run_process_wait):
    run_process_wait(cron_worker)
