class Object
  alias metaclass singleton_class
  alias eigenclass singleton_class
  def meta_eval &blk
    metaclass.instance_eval &blk
  end

  def meta_def name, &blk
    meta_eval { define_method name, &blk }
  end

  def class_def name, &blk
    class_eval {  define_method name, &blk }
  end
end










