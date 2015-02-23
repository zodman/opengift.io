class DrawBoard extends KanbanBox
	constructor: (options) ->
		super options.el
		@defaults = {
			headerSelector: '.js-project-header',
			tasksWrapperSelector: '.js-tasks-wrapper'
			idAttribute: 'id',
			tasks: {},
			dropZones: {},
			minHeight: 400
		}
		@projectRow = options.projectRow or {}
		@tasks = options.tasks or 
			@defaults.tasks
		@dropZones = options.dropZones or 
			@defaults.dropZones
		@id = @el.attr(options.idAttribute or 
			@defaults.idAttribute)
		@headerHeight = options.el.find(options.headerSelector or
			@defaults.headerSelector).height()
		@minHeight = options.minHeight or 
			@defaults.minHeight		
		@tasksWrapper = @el.find(
			options.tasksWrapperSelector or 
			@defaults.tasksWrapperSelector
		)
		do @initResizable
	getHeight: ->
		@el.height()
	store: ->
		window.localStorage.setItem(@getStoreKey(), @getHeight())
	restore: ->
		window.localStorage.getItem(@getStoreKey())
	getStoreKey: ->
		"#{@projectRow.storageKeyPrefix}_prj_#{@id}"
	resize:(height) ->
		if not height? or height < @minHeight
			height = @minHeight
		@el.css('height', height + 'px')
		@tasksWrapper.css('height', height - @headerHeight + 'px')
		for zone in @dropZones
			zone.resize(height - @headerHeight)
	initResizable: ->
		@el.resizable {
			handles: "s",
			minHeight: @minHeight,
			create: =>
				height = do @restore || do @getHeight
				@resize height
			stop: =>
				@resize(do @getHeight)
				do @store
		}

