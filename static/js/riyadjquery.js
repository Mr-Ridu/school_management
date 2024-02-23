$(document).ready(function () {
    $('.showdlt').on('click', function () {
        var tr = $(this).closest('tr');
        tr.fadeOut(1000, 'easeInOutExpo');
    });

    // $('#show_class_subjects').hover(function () {
    //     console.log("hoverd");
    // });

    // Script to handle displaying class details without modal
    $(document).ready(function () {
        $('.show_class_subjects').on('mouseenter', function () {
            var subjectName = $(this).data('subject');
            var classGrades = $(this).data('grades');
            $('#modalSubjectName').text('SUBJECT NAME:  ' + subjectName);
            $('#modalClassGrades').text('CLASS GRADE:  ' + classGrades);
            $('#detailsModal').removeClass('d-none');
        });
        $('.show_class_subjects').on('mouseleave', function () {
            $('#detailsModal').addClass('d-none');
        });
    });
});