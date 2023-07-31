type direction =
  | Right
  | Up
  | Diagonal
  | None;


let move_step = (begin_point, last_step, (end_x, end_y), cur_points) =>
  List.fold_left({(points, direction) => 
  switch(direction, last_step) {
  | Right, Up
  | Up, Right => points
  | _ => {
      let (x, y) as new_point = move_direction(begin_point, direction);
      if(x <= end_x && y <= end_y) [(new_point, direction), ...points];
      else points;
    }
  }},
                 cur_points,
[Right, Up, Diagonal]); 
  let move_direction = ((x, y)) =>
  fun
| Right => (x + 1, y)
| Up => (x, y + 1)
| Diagonal => (x + 1, y + 1)
| _ => failwith("invalid direction!");
