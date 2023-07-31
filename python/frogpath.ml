type direction = Right | Up | Diagnal | None

let move_direction (x, y) = function
  | Right -> x + 1, y
  | Up -> x, y + 1
  | Diagnal -> x + 1, y + 1
  | _ -> failwith "invalid direction!"

let move_step begin_point last_step (end_x, end_y) cur_points =
  List.fold_left (fun points direction ->
      match direction, last_step with
      | Right, Up
      | Up, Right -> points
      | _ ->
        let (x, y) as new_point = move_direction begin_point direction in
        if x <= end_x && y <= end_y then
          (new_point, direction)::points
        else points)
    cur_points
    [Right; Up; Diagnal]

let rec count_all begin_points end_point num =
  let next_points, ended_num = List.fold_left
      (fun (points, num) (point, last_direction) ->
         if point = end_point then (points, num + 1)
         else
           move_step point last_direction end_point points, num
      )
      ([], num)
      begin_points
  in match next_points with
  | [] -> ended_num
  | _ -> count_all next_points end_point ended_num

let count_paths begin_point end_point =
  count_all [(begin_point, None)] end_point 0

let () =
  let x = count_paths (0,0) (15, 15) in
  print_int x
