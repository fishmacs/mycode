class Creature2
   def self.traits( *arr )
     return @@traits if arr.empty?
     attr_accessor *arr
     arr.each do |trait|
       meta_def trait do |val|
         @@traits ||= {}
         @@traits[trait] = val
       end
     end
     class_def :initialize do
       self.class.traits.each do |k,v|
         instance_variable_set( "@#{k}", v )
       end
     end
   end
 end
