(function($) {
    $(document).ready(function() {
    	
    	$('.changelist-results .defaultObjectField').click(function(event){
    		/* Prevent from unchecking the default object */
    		if (! $(this).prop('checked')) {
    			console.debug("Don't uncheck the choosen one !");
    			return false;
    		}
    	});
    	
    	$('.changelist-results .defaultObjectField').change(function(event){
    		var $this = $(this);
    		var checked = $this.prop('checked');
    		
    		if (checked) {
    			/* uncheck other checkboxes from this column */
	    		var $td = $this.closest('td');
	    		var $tr = $td.parent();
	    		var colIndex = $tr.children().index($td) + 1;
	    		var $trs = $tr.siblings();
	    		var $tds = $trs.find(':nth-child(' + colIndex + ')');
	    		var $others = $tds.find('.defaultObjectField')
	    		$others.prop('checked', false);
    		}    		
    	});
    	
	});
})(django.jQuery)