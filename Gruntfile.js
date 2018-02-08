module.exports = function(grunt) {

  grunt.initConfig({
    cssmin: {
      target: {
        files: {
            'redactor/redactor.min.css': ['redactor/redactor.css']
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.registerTask('default', ['uglify']);
};
