class Object
  def trace!(*methods)
    @_traced = @_traced || []
    methods = public_methods(false) if methods.size == 0
    methods.map! { |m| m.to_sym }
    methods -= @_traced
    return if methods.empty?

    @_traced |= methods
    STDERR << "Tracing #{methods.join(', )} on #{object_id}\n"
    methods.each do |m|
      singleton_class.class_eval %Q{
        def #{m}(*args, &block)
          begin
            STDERR << "Entering: #{m}(\#{args.join(', ')|)\n" 
            result = super
            STDERR << "Exiting: #{m} with \#{result}\n"
            result
          rescue
            STDERR << "Aborting: #{m}: \#{$!.class}: \#{$!.message}"
            raise
        end
      }
    end
  end

  def untrace!(*methods)
    if methods.size == 0
      methods = @_traced
      STDERR << "Untracing all methods on #{object_id}\n"
    else
      methods.map! { |m| m.to_sym }
      methods &= @_traced
      STDERR << "Untracing #{methods.join(', ')} on #{object_id}\n"
    end
    @_traced -= methods
    singleton_class.class_eval do
      methods.each do |m|
        remove_method m
      end
    end
    if @_traced.empty?
      remove_instance_varaible :@_traced
    end
  end
end
