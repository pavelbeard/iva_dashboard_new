const chartTypes = [
    {
        id: 'group.modules',
        charts: [
            {
                id: 'chart.modules.cpu.usage',
                query: 'label_keep(label_move((sum(rate(namedprocess_namegroup_cpu_seconds_total) * 100) by (groupname)), "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.memory.resident',
                query: 'label_keep(label_move(namedprocess_namegroup_memory_bytes{memtype="resident"} / 1048576, "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.disk.read',
                query: 'label_keep(label_move(rate(namedprocess_namegroup_read_bytes_total) / 1024, "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.disk.write',
                query: 'label_keep(label_move(rate(namedprocess_namegroup_write_bytes_total) / 1024, "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.processes',
                query: 'label_keep(label_move(namedprocess_namegroup_num_procs, "groupname","__name__"),"__name__")'
            },
            {
                id: 'chart.modules.threads',
                query: 'label_keep(label_move(namedprocess_namegroup_num_threads, "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.fileDescriptors',
                query: 'label_keep(label_move(namedprocess_namegroup_open_filedesc, "groupname", "__name__"), "__name__")'
            },
            {
                id: 'chart.modules.hiccups.monotonic',
                query: 'label_keep(label_move(monotonic_hiccup_max_ms / 1000, "service", "__name__"), "__name__")',
                beginAtZero: true
            },
            {
                id: 'chart.modules.hiccups.nonMonotonic',
                query: 'label_keep(label_move(non_monotonic_hiccup_max_ms / 1000, "service", "__name__"), "__name__")',
                beginAtZero: true
            }
        ]
    }
]