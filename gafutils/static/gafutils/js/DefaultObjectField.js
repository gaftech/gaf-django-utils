(function($) {
    $(document).ready(function() {
    	
    	$('#result_list .defaultObjectField').click(function(event){
    		/* Prevent from unchecking the default object */
    		if (! $(this).attr('checked')) {
    			console.debug("Don't uncheck the choosen one !");
    			return false;
    		}
    	});
    	
    	$('#result_list .defaultObjectField').change(function(event){
    		var $this = $(this);
    		var checked = $this.attr('checked');
    		
    		if (checked) {
    			/* uncheck other checkboxes from this column */
	    		var $td = $this.closest('td');
	    		var $tr = $td.parent();
	    		var colIndex = $tr.children().index($td) + 1;
	    		var $trs = $tr.siblings();
	    		var $tds = $trs.find(':nth-child(' + colIndex + ')');
	    		var $others = $tds.find('.defaultObjectField')
	    		$others.attr('checked', false);
    		}    		
    	});
    	
	});
})(django.jQuery)