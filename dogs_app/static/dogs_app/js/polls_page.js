$(document).ready(function () {
    const table = $('#pollsTable').DataTable({
        "order": [[0, "desc"]],
        "columnDefs": [
            {
                "targets": 0,
                "type": "date",
                "render": function (data, type, row, meta) {
                    const parsedDate = moment(data, ["MMM. D, YYYY, h:mm a", "MMMM D, YYYY, h:mm a", "MMMM D, YYYY, h:mm p"], true);
                    if (parsedDate.isValid()) {
                        if (type === 'sort') {
                            return parsedDate.format("YYYY-MM-DD HH:mm:ss");
                        }
                        return parsedDate.format("MMMM D, YYYY, h:mm a");
                    } else {
                        return data;
                    }
                }
            },
            {
                "targets": 2,
                "orderable": false  // Disable sorting for the empty space column
            },
            {
                "targets": 3,
                "orderable": false  // Disable sorting for the actions column
            }
        ],
        "drawCallback": function (settings) {
            let setCount = 0;
            $('#pollsTable tbody tr:not(.content-row)').each(function () {
                const content = $(this).data('content');
                const contentRow = $('<tr class="content-row second-row"><td colspan="4"></td></tr>');
                contentRow.find('td').html(content);

                $(this).after(contentRow);

                // Apply background color based on the set count
                const backgroundColor = (setCount % 2 === 0) ? '#F8F9F9' : '#ffffff';

                $(this).css('background-color', backgroundColor);
                contentRow.css('background-color', backgroundColor);

                // Increment the set count for the next row
                setCount++;
            });
        }
    });
});

