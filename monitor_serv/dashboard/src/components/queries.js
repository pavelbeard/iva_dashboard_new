export const system = {
    cpuData: 'query?query=sum by (mode,instance) (label_keep(rate(node_cpu_seconds_total), "mode")) * 100 / distinct(label_value(node_cpu_seconds_total, "cpu"))',
    cpuCores: 'query?query=label_keep(alias(count(node_cpu_seconds_total{mode="idle"}) without (cpu, mode), "Cpu cores"), "__name__", "device")',
    la: 'label_keep((node_load1, node_load5, node_load15), "__name__")',
    memory: 'query?query=label_keep(('
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
    errors: '',
    throughput: 'query?query=label_keep(('
                + 'alias((rate(node_network_receive_bytes_total) * 8 / 1024), "RX"),'
                + 'alias((rate(node_network_transmit_bytes_total) * 8 / 1024), "TX")'
                + '), "__name__", "device")',
    packets: '',

}

export const disk = {
    rootSpace: 'query?query=label_keep(' +
                'label_match(' +
                '(alias(node_filesystem_size_bytes / 1073741824, "Total"),' +
                'alias((node_filesystem_size_bytes-node_filesystem_free_bytes) / 1073741824, "Used"), ' +
                'alias((node_filesystem_free_bytes-node_filesystem_avail_bytes) / 1073741824, "Reserved"), ' +
                'alias(node_filesystem_avail_bytes / 1073741824, "Free")), ' +
                '"mountpoint", "/|/etc/hosts"), "__name__", "device")',
    merges: '',
    io: 'query?query=label_keep((alias(rate(node_disk_read_bytes_total) / 1048576, "Reads"), alias(rate(node_disk_written_bytes_total) / 1048576, "Writes")), "__name__", "device")',
    operations: '',
    times: '',
}

export const modules = {
    processCount: 'query?query=label_keep(alias(sum by (instance) (namedprocess_namegroup_num_procs), "Process count"), "__name__")',
    cpuUsage: '',
    memoryResident: '',
    diskRead: '',
    diskWrite: '',
    processes: '',
    threads: '',
    fileDescriptors: '',
}