require 'fileutils'

# I 've a extra maven repository in ~/.ivy2/repository/ by mistake, sync it to ~/.m2/repository
def sync(src, des)
  if File.file? src
    FileUtils.copy(src, des) unless File.exist? des
  elsif File.directory? src
    FileUtils.makedirs des unless File.exist? des
    Dir[File.join(src, '*')].each do |f|
      sync(f, File.join(des, File.basename(f)))
    end
  end
end

src, des = ARGV
sync(src, des)
