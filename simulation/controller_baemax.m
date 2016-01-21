% main control code - assumes full state knowledge
%
%
% Modified:
%   2/11/2014 - R. Beard
%   2/18/2014 - R. Beard
%   2/24/2014 - R. Beard
%   1/4/2016  - R. Beard
%

% this first function catches simulink errors and displays the line number

% -11.5 * P.field_width/12 = -11.5 * P.field_width/12;
% -11 * P.field_width/12 = -11 * P.field_width/12;
% 75 * (pi/180) = 75 * (pi/180); % 75 degrees converted to radians

function v_c=controller_home(uu,P)
    try
        v_c=controller_home_(uu,P);
    catch e
        msgString = getReport(e);
        fprintf(2,'\n%s\n',msgString);
        rethrow(e);
    end
end



% main control function
function v_c=controller_home_(uu,P)

    % process inputs to function
    % robots - own team
    for i=1:P.num_robots,
        robot(:,i)   = uu(1+3*(i-1):3+3*(i-1));
    end
    NN = 3*P.num_robots;

    % robots - opponent
    for i=1:P.num_robots,
        opponent(:,i)   = uu(1+3*(i-1)+NN:3+3*(i-1)+NN);
    end
    NN = NN + 3*P.num_robots;

    % ball
    ball = [uu(1+NN); uu(2+NN)];
    NN = NN + 2;

    % score: own team is score(1), opponent is score(2)
    score = [uu(1+NN); uu(2+NN)];
    NN = NN + 2;

    % current time
    t      = uu(1+NN);

    % robot #1 positions itself behind ball and rushes the goal.
    %v1 = play_rush_goal(robot(:,1), ball, P);
    %v1 = [0;0;90*pi/180];

    %v1 = skill_play_midfield(robot(:,2), ball, P);

    % robot #2 stays on line, following the ball, facing the goal
    %v2 = skill_follow_ball_on_line(robot(:,2), ball, -2*P.field_width/3, P);
    %v2 = skill_play_goalie(robot(:,2), ball, P);

    % output velocity commands to robots
    %v1 = utility_saturate_velocity(v1,P);
    %v2 = utility_saturate_velocity(v2,P);


    % v_c = [v1; v2];
    v_c = strategy_strong_defense(robot, opponent, ball, P, t);
end

%%-------------------------------------------
%% Strategies
%%-------------------------------------------

%-----------------------------------------
% strategy - strategy_strong_defense
% - V1 will always be rushing
% - V2 switches between midfield and goalie
function v_c = strategy_strong_defense(robot, opponent, ball, P, t)
    defense = 0;
    offense = 1;
    playtype = offense;

    % V2 is always rushing

    % v1 = play_rush_goal(robot(:,1), ball, P);

    v2 = skill_play_goalie(robot(:,2), ball, P);
    v1 = play_rush_goal(robot(:,1), ball, P);

    % if the ball goes to the left of the mid point line V2 switches to goalie,
    % otherwise it is midfielder
    % if(ball(1) < 0)
    %     v2 = skill_play_goalie(robot(:,2), ball, P);
    % else
    %     % v2 = skill_play_midfield(robot(:,2), ball, P);
    %      v2 = play_rush_goal(robot(:,2), ball, P);
    % end

    v1 = utility_saturate_velocity(v1,P);
    v2 = utility_saturate_velocity(v2,P);
    v_c = [v1; v2];
end


%-----------------------------------------
% play - rush goal
%   - go to position behind ball
%   - if ball is between robot and goal, go to goal
% NOTE:  This is a play because it is built on skills, and not control
% commands.  Skills are built on control commands.  A strategy would employ
% plays at a lower level.  For example, switching between offense and
% defense would be a strategy.
function v = play_rush_goal(robot, ball, P)

  % normal vector from ball to goal
  n = P.goal-ball;
  n = n/norm(n);

  % compute position 10cm behind ball, but aligned with goal.
  position = ball - 0.2*n;

  if norm(position - robot(1:2)) < .21
      v = skill_go_to_point(robot, P.goal, P);
  else
      v = skill_go_to_point(robot, position, P);
  end

end

%-----------------------------------------
% skill - follow ball on line
%   follows the y-position of the ball, while maintaining x-position at
%   x_pos.  Angle always faces the goal.
function v=skill_follow_ball_on_line(robot, ball, x_pos, P)

    % control x position to stay on current line
    vx = -P.control_k_vx*(robot(1)-x_pos);

    % control y position to match the ball's y-position
    vy = -P.control_k_vy*(robot(2)-ball(2));

    % control angle to -pi/2
    theta_d = atan2(P.goal(2)-robot(2), P.goal(1)-robot(1));
    omega = -P.control_k_phi*(robot(3) - theta_d);

    v = [vx; vy; omega];
end

%-----------------------------------------
% skill - go to point
%   follows the y-position of the ball, while maintaining x-position at
%   x_pos.  Angle always faces the goal.
function v=skill_go_to_point(robot, point, P)

    % control x position to stay on current line
    vx = -P.control_k_vx*(robot(1)-point(1));

    % control y position to match the ball's y-position
    vy = -P.control_k_vy*(robot(2)-point(2));

    % control angle to -pi/2
    theta_d = atan2(P.goal(2)-robot(2), P.goal(1)-robot(1));
    omega = -P.control_k_phi*(robot(3) - theta_d);

    v = [vx; vy; omega];
end


function v=skill_play_goalie(robot, ball, P)

    % control x position to stay on current line
    vx = -P.control_k_vx*(robot(1)--11.5 * P.field_width/12);

    % control y position to match the ball's y-position
    %vy = -P.control_k_vy*(robot(2)-ball(2));
    vy = -20 * (robot(2) - ball(2));

    if (ball(2) > (1/6)*P.field_width || ball(2)< -(1/6)*P.field_width)
        if (robot(2) > (1/6)*P.field_width || robot(2)< -(1/6)*P.field_width)
            vy = 0;
        end
    end

    % control angle to -pi/2
    theta_d = atan2(ball(2)-robot(2), ball(1)-robot(1));

    if(theta_d > 75 * (pi/180))
        theta_d = 75 * (pi/180) - 2*pi/180;
    end

    if(theta_d < -75 * (pi/180))
        theta_d = -75 * (pi/180) + 2*pi/180 ;
    end

    omega = -P.control_k_phi * (robot(3) - theta_d);

    v = [vx; vy; omega];
end

function v=skill_play_midfield(robot, ball, P)

    vx = -P.control_k_vx*(robot(1) + P.field_width/2);

    % control y position to match the ball's y-position
    vy = -P.control_k_vy*(robot(2)-ball(2));

    % control angle to -pi/2
    theta_d = atan2(P.goal(2)-robot(2), P.goal(1)-robot(1));
    omega = -P.control_k_phi*(robot(3) - theta_d);

    v = [vx; vy; omega];

end

%------------------------------------------
% utility - saturate_velocity
%   saturate the commanded velocity
%
function v = utility_saturate_velocity(v,P)
    if v(1) >  P.robot_max_vx,    v(1) =  P.robot_max_vx;    end
    if v(1) < -P.robot_max_vx,    v(1) = -P.robot_max_vx;    end
    if v(2) >  P.robot_max_vy,    v(2) =  P.robot_max_vy;    end
    if v(2) < -P.robot_max_vy,    v(2) = -P.robot_max_vy;    end
    if v(3) >  P.robot_max_omega, v(3) =  P.robot_max_omega; end
    if v(3) < -P.robot_max_omega, v(3) = -P.robot_max_omega; end
end
