config =

    src: 'src'
    dest: 'backend/static'
    temp: '.temp'

    clean: ['<%= dest %>/scripts.js', '<%= dest %>/styles.css' ]

    jade:
        main:
            src: '<%= src %>/pages/index.jade'
            dest: '<%= dest %>/index.html'

    coffee:
        main:
            src: '<%= src %>/scripts/*.coffee'
            dest: '<%= temp %>/coffee.js'

    stylus:
        main:
            src: '<%= src %>/styles/styles.styl'
            dest: '<%= temp %>/stylus.css'

    cssmin:
        main:
            files:
                '<%= dest %>/styles.css': '<%= dest %>/styles.css'

    concat:
        js:
            src: [
                'components/jquery/dist/jquery.js',
                '<%= src %>/scripts/*.js',
                '<%= temp %>/coffee.js'
            ]
            dest: '<%= dest %>/scripts.js'
        css:
            src: [
                '<%= src %>/styles/*.css',
                '<%= temp %>/stylus.css']
            dest: '<%= dest %>/styles.css'

    uglify:
        main:
            src: '<%= dest %>/scripts.js'
            dest: '<%= dest %>/scripts.js'

    watch:
        options:
            livereload: true
        stylus:
            files: ['<%= src %>/styles/*.styl']
            tasks: ['stylus', 'concat:css']
        css:
            files: ['<%= src %>/styles/*.css']
            tasks: ['concat:css']
        coffee:
            files: ['<%= src %>/scripts/*.coffee']
            tasks: ['coffee', 'concat:js']
        js:
            files: ['<%= src %>/scripts/*.js']
            tasks: ['concat:js']

module.exports = (grunt) ->
    require('time-grunt') grunt
    grunt.initConfig(config)
    require('jit-grunt') grunt

    grunt.registerTask 'build', ['stylus', 'coffee', 'concat']
    grunt.registerTask 'polish', ['clean', 'build', 'uglify', 'cssmin']
    grunt.registerTask 'default', ['build', 'watch']
