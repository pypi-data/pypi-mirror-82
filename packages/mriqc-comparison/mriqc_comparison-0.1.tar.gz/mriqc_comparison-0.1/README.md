# mriqc_comparison
Compare your MRIQC results with other similar runs

This is a tool that allows you to compare [MRIQC](https://github.com/poldracklab/mriqc) Image Quality Metrics (IQMs) corresponding to certain runs with IQMs from other runs collected with similar parameters (so that the comparison is meaningful). For example, it allows you to compare the IQMs for your runs with all the other runs collected in the same scanner; or to compare your IQMs with those from a different scanner.

[MRIQC](https://github.com/poldracklab/mriqc) does give you the option to generate a report comparing the IQMs for all runs in a given BIDS project. However, it does not allow you to compare IQMs across your projects, or with a colleague's data. This tool comes in to fill that gap.

To generate these comparison reports, you can get the IQMs from the `group_*.tsv` files generaged by the [MRIQC](https://github.com/poldracklab/mriqc) group reports, or you can get them online: [MRIQC](https://github.com/poldracklab/mriqc) sends an annonymized list of the IQMs to a public server (hosted by NIH). The BIDS project name, subject's ID and run name are scrubbed from the data, but if you know the `DeviceSerialNumber` for a certain scanner, you can download all the IQMs corresponding to that scanner stored in the public server. Alternatively, you could also download all the data corresponding to a given scanner model (e.g., "Siemens Prisma")

Once you have the IQMs you want to use in your comparison, you can generate a group report, showing all of the runs, or showing only those runs that were acquired with certain scanning parameters, etc. Also, you can have the group report highlighting certain runs; for example, you can generate a report showing the IQMs of all functional runs collected in your center, highlighting those corresponding to your study, to see if you get similar data to other labs in your center.

The tool is written in Python3, and requires [MRIQC](https://github.com/poldracklab/mriqc).
