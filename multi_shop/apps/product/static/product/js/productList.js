$(document).ready(function () {

    function updateProducts(response) {
        $('.my-product').remove();
        response.products.forEach(function (value) {
            var myDiv = `
                <div class="col-lg-4 col-md-6 col-sm-6 pb-1 my-product">
                    <div class="product-item bg-light mb-4">
                        <div class="product-img position-relative overflow-hidden">
                            <img class="img-fluid w-100" src="${value.imageUrl}" alt="">
                            <div class="product-action">
                                <a class="btn btn-outline-dark btn-square" href="#"><i class="fa fa-shopping-cart"></i></a>
                                <a class="btn btn-outline-dark btn-square btn-like" href="${value.urlLike}"><i class="${value.isLiked ? 'fas' : 'far'} fa-heart"></i></a>
                                <a class="btn btn-outline-dark btn-square" href="#"><i class="fa fa-sync-alt"></i></a>
                                <a class="btn btn-outline-dark btn-square" href="#"><i class="fa fa-search"></i></a>
                            </div>
                        </div>
                        <div class="text-center py-4">
                            <a class="h6 text-decoration-none text-truncate" href="${value.redirectUrl}">${value.name}</a>
                            <div class="d-flex align-items-center justify-content-center mt-2">
                                <h5>$${value.bestDiscountedPrice}</h5>
                                ${value.price !== value.bestDiscountedPrice ? `<h6 class="text-muted ml-2"><del>${value.price}</del></h6>` : ''}
                            </div>
                        </div>
                    </div>
                </div>`;
            $('#before-products').before(myDiv);
        });
    }

    function updatePagination(response, filterParams) {
        if (response.pagination.has_other_pages) {
            var paginationHtml = '<ul class="pagination justify-content-center">';
            if (response.pagination.has_previous) {
                paginationHtml += `<li class="page-item"><a class="page-link" href="?${filterParams}&page=${response.pagination.previous_page_number}">Previous</a></li>`;
            }
            for (var i = 1; i <= response.pagination.num_pages; i++) {
                paginationHtml += `<li class="page-item ${i === response.pagination.current_page ? 'active' : ''}"><a class="page-link" href="?${filterParams}&page=${i}">${i}</a></li>`;
            }
            if (response.pagination.has_next) {
                paginationHtml += `<li class="page-item"><a class="page-link" href="?${filterParams}&page=${response.pagination.next_page_number}">Next</a></li>`;
            }
            paginationHtml += '</ul>';
            $('#pagination').html(paginationHtml);
        } else {
            $('#pagination').empty();
        }
    }

    function ajaxRequest(filterParams) {
        var currentParams = new URLSearchParams(window.location.search);
        currentParams.delete('page');
        var fullParams = filterParams + '&' + currentParams.toString();

        $.ajax({
            url: '?' + fullParams,
            type: 'GET',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function (response) {
                updateProducts(response);
                updatePagination(response, fullParams);
            },
            error: function (xhr) {
                alert(xhr.responseText);
            }
        });
    }

    $('#submitAll').click(function () {
        var filterParams = $('#form1, #form2, #form3').serialize();
        ajaxRequest(filterParams);
    });

    $(document).on('click', '.page-link', function (e) {
        e.preventDefault();
        ajaxRequest($(this).attr('href').split('?')[1]);
    });

});
