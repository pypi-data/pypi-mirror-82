import numpy as np

from libensemble.tools.alloc_support import avail_worker_ids, sim_work, gen_work, count_gens


def give_sim_work_first(W, H, sim_specs, gen_specs, alloc_specs, persis_info):
    """
    This allocation function gives (in order) entries in ``H`` to idle workers
    to evaluate in the simulation function. The fields in ``sim_specs['in']``
    are given. If all entries in `H` have been given to be evaluated, a worker
    is told to call the generator function, provided this wouldn't result in
    more than ``alloc_specs['user']['num_active_gen']`` active generators. Also allows
    for a ``'batch_mode'``.

    .. seealso::
        `test_old_aposmm_with_gradients.py <https://github.com/Libensemble/libensemble/blob/develop/libensemble/tests/regression_tests/test_old_aposmm_with_gradients.py>`_ # noqa
    """

    Work = {}
    gen_count = count_gens(W)

    for i in avail_worker_ids(W):

        # Find indices of H that are not yet allocated
        if persis_info['next_to_give'] < len(H):
            # Give sim work if possible
            sim_work(Work, i, sim_specs['in'], [persis_info['next_to_give']], [])
            persis_info['next_to_give'] += 1

        elif gen_count < alloc_specs['user'].get('num_active_gens', gen_count+1):
            lw = persis_info['last_worker']

            last_size = persis_info.get('last_size')
            if len(H):
                # Don't give gen instances in batch mode if points are unfinished
                if (alloc_specs['user'].get('batch_mode')
                    and not all(np.logical_or(H['returned'][last_size:],
                                              H['paused'][last_size:]))):
                    break
                # Don't call APOSMM if there are runs going but none need advancing
                if len(persis_info[lw]['run_order']):
                    runs_needing_to_advance = np.zeros(len(persis_info[lw]['run_order']), dtype=bool)
                    for run, inds in enumerate(persis_info[lw]['run_order'].values()):
                        runs_needing_to_advance[run] = H['returned'][inds[-1]]

                    if not np.any(runs_needing_to_advance):
                        break

            persis_info['last_size'] = len(H)

            # Give gen work
            persis_info['total_gen_calls'] += 1
            gen_count += 1
            gen_work(Work, i, gen_specs['in'], range(len(H)), persis_info[lw])

            persis_info['last_worker'] = i

    return Work, persis_info
