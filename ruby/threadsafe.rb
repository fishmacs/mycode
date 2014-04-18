class Module
  def create_alias(original, prefix='alias')
    aka = "#{prefix}_#{original}"
    aka.gsub!(/([\=\|\&\+\-\*\/\^\!\?\~\%\<\>\[\]])/) {
      num = $1[0]
      num = num.ord if num.is_a? String
      '_' + num.to_s
    }
    aka += "_" while method_defined? aka or private_method_defined? aka
    aka = aka.to_sym
    alias_method aka, original
    aka
  end

  def synchronize_method(m)
    aka = create_alias(m, "unsync")
    class_eval %Q{
      def #{m}(*args, &block)
        synchronized(self) { #{aka}(*args, &block) }
      end
    }
  end
end
  
def synchronized(*args)  
  if args.size == 1 && block_given?
    args[0].mutex.synchronize { yield }
  elsif args.size == 1 and not args[0].is_a? Symbol and not block_given?
    SynchronizedObject.new(args[0])
  elsif is_a? Module and not block_given?
    if(args.size > 0)
      args.each { |m| synchronize_method(m) }
    else
      singleton_class.class_eval do
        define_method :method_added do |name|
          singleton_class.class_eval { remove_method :method_added }
          synchronize_method name
        end
      end
    end
  else
    raise ArgumentError, 'Invalid arguments to synchronize()'
  end
end

