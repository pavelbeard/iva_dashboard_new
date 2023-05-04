export const system = {
    cpuData: 'sum by (mode,instance) (label_keep(rate(node_cpu_seconds_total), "mode")) * 100 / distinct(label_value(node_cpu_seconds_total, "cpu"))',
    cpuCores: 'label_keep(alias(count(node_cpu_seconds_total{mode="idle"}) without (cpu, mode), "Cpu cores"), "__name__", "device")',
    la: 'label_keep((node_load1, node_load5, node_load15), "__name__")',
    memory: 'label_keep(('
                + 'alias(node_memory_MemTotal_bytes / 1073741824, "Total"),'
                + 'alias(node_memory_Buffers_bytes / 1073741824, "Buffered"),'
                + 'alias(node_memory_Slab_bytes / 1073741824, "Slab"),'
                + 'alias(node_memory_MemFree_bytes / 1073741824, "Free"),'
                + 'alias(node_memory_MemAvailable_bytes / 1073741824, "Available"),'
                + 'alias(node_memory_Cached_bytes / 1073741824, "Cached")'
                + '), "__name__")',
    contextSwitches: 'label_keep(alias(rate(node_context_switches_total), "Context switches"), "__name__")',
    uptime: 'label_keep((alias((node_time_seconds-node_boot_time_seconds) / 86400, "Uptime")), "__name__")',
}

export const network = {
    errors: 'label_keep(('
                        + 'alias(node_network_receive_errs_total, "RX errors"),'
                        + 'alias(node_network_transmit_errs_total, "TX errors")' +
                        '), "__name__", "device")',
    throughput: 'label_keep(('
                + 'alias((rate(node_network_receive_bytes_total) * 8 / 1024), "RX"),'
                + 'alias((rate(node_network_transmit_bytes_total) * 8 / 1024), "TX")'
                + '), "__name__", "device")',
    packets: 'label_keep(('
                        + 'alias(rate(node_network_receive_packets_total), "RX packets/s"),'
                        + 'alias(rate(node_network_transmit_packets_total), "TX packets/s")'
                        + '), "__name__", "device")',
}

export const disk = {
    rootSpace: 'label_keep(' +
                'label_match(' +
                '(alias(node_filesystem_size_bytes / 1073741824, "Total"),' +
                'alias((node_filesystem_size_bytes-node_filesystem_free_bytes) / 1073741824, "Used"), ' +
                'alias((node_filesystem_free_bytes-node_filesystem_avail_bytes) / 1073741824, "Reserved"), ' +
                'alias(node_filesystem_avail_bytes / 1073741824, "Free")), ' +
                '"mountpoint", "/|/etc/hosts"), "__name__", "device")',
    merges: 'label_keep((alias(rate(node_disk_reads_merged_total), "Reads merged"), alias(rate(node_disk_writes_merged_total), "Writes merged")), "__name__", "device")',
    io: 'label_keep((alias(rate(node_disk_read_bytes_total) / 1048576, "Reads"), alias(rate(node_disk_written_bytes_total) / 1048576, "Writes")), "__name__", "device")',
    operations: 'label_keep((alias(rate(node_disk_reads_completed_total), "Reads"), alias(rate(node_disk_writes_completed_total), "Writes")), "__name__", "device")',
    times: 'label_keep((alias(rate(node_disk_read_time_seconds_total) / rate(node_disk_reads_completed_total),"Avg time/op read"), alias(rate(node_disk_write_time_seconds_total) / rate(node_disk_writes_completed_total), "Avg time/op write"), alias(rate(node_disk_io_time_seconds_total) * 100, "I/O utilization")), "__name__", "device")',
}

export const modules = {
    states: 'namedprocess_namegroup_states',
    cpuUsage: 'label_keep(label_move((sum(rate(namedprocess_namegroup_cpu_seconds_total) * 100) by (groupname)), "groupname", "__name__"), "__name__")',
    memoryResident: 'label_keep(label_move(namedprocess_namegroup_memory_bytes{memtype="resident"} / 1048576, "groupname", "__name__"), "__name__")',
    diskRead: 'label_keep(label_move(rate(namedprocess_namegroup_read_bytes_total) / 1024, "groupname", "__name__"), "__name__")',
    diskWrite: 'label_keep(label_move(rate(namedprocess_namegroup_write_bytes_total) / 1024, "groupname", "__name__"), "__name__")',
    threads: 'label_keep(label_move(namedprocess_namegroup_num_threads, "groupname", "__name__"), "__name__")',
    processes: 'label_keep(label_move(namedprocess_namegroup_num_procs, "groupname","__name__"),"__name__")',
    fileDescriptors: 'label_keep(label_move(namedprocess_namegroup_open_filedesc, "groupname", "__name__"), "__name__")',
    hiccupsMonotonic: 'label_keep(label_move(monotonic_hiccup_max_ms / 1000, "service", "__name__"), "__name__")',
    hiccupsNonMonotonic: 'label_keep(label_move(non_monotonic_hiccup_max_ms / 1000, "service", "__name__"), "__name__")'
}