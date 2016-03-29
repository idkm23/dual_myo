function new_t = align_signal(s, t, w, hasTime)
% every row of s or t is a time series
% every column is dimensions of signal at one time point
% w size is symmetric. w=5 means the window has size 11.

if ~ exist('hasTime')
    hasTime = true;
end
    

if hasTime
    s = s(:, 2:end);
    t = t(:, 2:end);
end

[Dist, D, k, p]=dtw(s, t, w);
%Dist is unnormalized distance between t and r
%D is the accumulated distance matrix
%k is the normalizing factor
%p is the optimal path

% lower to higher
p = flip(p);

warped_t = t(p(:,2), :);
new_t = zeros(size(s));

for i=1:size(warped_t,1)
    new_t(p(i,1), :)=warped_t(i, :);
end

if hasTime
    Ts = 1:size(s, 1);
    new_t = [Ts', new_t];
end

end
