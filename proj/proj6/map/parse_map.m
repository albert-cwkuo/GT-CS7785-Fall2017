% compute branching points of the skeleton map
I=imread('./sim/map.pgm');
Is=im2single(I);
Ibw=imbinarize(Is,0.9);
Ishrk=bwmorph(Ibw,'spur');
Icln=bwmorph(Ishrk,'clean');
Iskel=bwmorph(Icln,'skel', Inf);
Ibpts=bwmorph(Iskel,'branchpoints');

% visualize branching points
Ir=I;
Ir(Iskel(:))=0;
Ir(Ibpts(:))=255;
Ig=I;
Ig(Iskel(:))=255;
Ig(Ibpts(:))=0;
Ib=I;
Ib(Iskel(:))=0;
Ib(Ibpts(:))=0;
I3c=cat(3,Ir,Ig,Ib);
f=figure;
imshow(I3c)

% parse graph
[row, col] = ind2sub(size(Ibpts),find(Ibpts));
targets=[col,row];
num_targets = size(targets,1);
Iskel = int8(Iskel);
Iskel(Ibpts(:)) = -1;
map_graph = cell(num_targets, 2);
for i=1:num_targets
    text(targets(i,1),targets(i,2),num2str(i),'Color','blue', 'FontSize',14);
    map_graph{i,1} = targets(i,:);
    [map_graph{i,2}, ~] = search_neighbor(Iskel,targets(i,1),targets(i,2),targets);
end
% saveas(f,'parsed_map.png');
save('map_graph.mat', 'map_graph')

function [results, I] = search_neighbor(I, x, y, targets)
I(y,x)=0;
% find target
hit = find(I(y-1:y+1,x-1:x+1) == -1);
if size(hit,1) ~= 0
    [r,c] = ind2sub([3,3],hit);
    y=y+r-2;
    x=x+c-2;
    
    num_target = size(targets,1);
    for i=1:num_target
        if targets(i,1) == x & targets(i,2) == y
            results = [i];
            return
        end
    end
end
% end of search
miss = find(I(y-1:y+1,x-1:x+1) == 0);
if size(miss,1) == 9
    results = [-1];
    return
end
% keep searching
route = find(I(y-1:y+1,x-1:x+1) == 1);
[r,c] = ind2sub([3,3],route);
num_route = size(r,1);
results=[];
for i=1:num_route
    yi=y+r(i)-2;
    xi=x+c(i)-2;
    [search_result, I] = search_neighbor(I, xi, yi, targets);
    if all(search_result ~= -1)
        results = [results, search_result];
    end
end
end