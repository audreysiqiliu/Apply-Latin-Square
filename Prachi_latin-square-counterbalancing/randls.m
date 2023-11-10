function rc = randls(N, varargin)
% RANDLS   Generate a uniformly distributed random Latin square.
%    LS = RANDLS(N) returns an NxN matrix representative of a Latin square,
%    picked from an approximately uniform distribution on the space of
%    Latin squares of order N. The Markov chain Monte Carlo algorithm
%    proposed by Jacobson & Matthews [1] is used with the implementational
%    ideas proposed by Gallego Sagastume [2].
%    
%    LS = RANDLS(N, 'maxIter', I) performs I iterations at most (100000
%    by default).
% 
%    LS = RANDLS(N, 'nProper', P) iterates until P proper Latin squares
%    are obtained (2400 by default).
% 
%    [1] M. Jacobson, P. Matthews, "Generating uniformly distributed random
%        Latin squares", Journal of Combinatorial Designs, vol. 4, no. 6,
%        pp. 405-437, 1996.
%    [2] I. Gallego Sagastume, "Generation of random latin squares step by
%        step and graphically", XX Congreso Argentino de Ciencias
%        de la Computación (Buenos Aires, 2014)
%    
%    Jakub Wagner, August 17, 2020
%    Institute of Radioelectronics and Multimedia Technology
%    Warsaw University of Technology
% Parse input arguments
parser = inputParser;
addRequired(parser, 'N', @isnumeric);
addParameter(parser, 'maxIter', 100000, @isnumeric);
addParameter(parser, 'nProper', 2400, @isnumeric);
parse(parser, N, varargin{:});
I = parser.Results.maxIter;
NP = parser.Results.nProper;
% Generate initial Latin square
rc = zeros(N,N);
rc(1,:) = randperm(N);
for n = 2:N
    rc(n,:) = circshift(rc(n-1,:),-1);
end
% Determine remaining representations of initial Latin square
% (row-symbol and column-symbol planes)
rs = zeros(N,N);
cs = zeros(N,N);
for r = 1:N
    for c = 1:N
        rs(r,rc(r,c)) = c;
        cs(c,rc(r,c)) = r;
    end
end
proper = true;  % current (initial) Latin square is proper
np = 0;         % number of proper squares obtained
for i = 1:I
    
    if proper
        % Current square is proper
        np = np + 1;    % increment number of obtained proper squares
        rcLast = rc;    % remember last proper square
        
        % Pick a random 0-cell and the 1-cells in the lines which pass
        % through that cell
        r0 = randi(N);
        c0 = randi(N);
        s1 = rc(r0,c0);
        s0 = randi(N-1);
        if s0 >= s1
            s0 = s0+1;
        end
        r1 = cs(c0,s0);
        c1 = rs(r0,s0);
        
        % Update the 3 lines which pass through the selected cell
        rc(r0,c0) = s0;
        rs(r0,s0) = c0;
        cs(c0,s0) = r0;
        
    else
        % Current square is improper
        
        % Pick the (-1)-cell
        r0 = r1;
        c0 = c1;
        s0 = s1;
        
        % Pick random 1-cells in the lines which pass through the (-1)-cell
        % [r2, c2 and s2 are the "extra" 1-cells from the last iteration;
        % cs(c0,s0), rs(r0,s0) and rc(r0,c0) are the "previous" 1-cells,
        % i.e. those which were there before the last iteration]
        
        if rand <= 0.5
            % The previous 1-cell is selected; update corresponding line
            r1 = cs(c0,s0);
            cs(c0,s0) = r2;
        else
            % The "extra" 1-cell is selected; no need to update
            r1 = r2;
        end
        
        if rand <= 0.5
            % Analogous to rows; see above
            c1 = rs(r0,s0);
            rs(r0,s0) = c2;
        else
            c1 = c2;
        end
        
        if rand <= 0.5
            % Analogous to rows; see above
            s1 = rc(r0,c0);
            rc(r0,c0) = s2;
        else
            s1 = s2;
        end
    end
    
    % Update remaining lines except those which pass through "target" cell
    rc(r0,c1) = s1;
    rc(r1,c0) = s1;
    rs(r0,s1) = c1;
    rs(r1,s0) = c1;
    cs(c0,s1) = r1;
    cs(c1,s0) = r1;
        
    if rc(r1,c1) == s1
        % Resulting square will be proper
        proper = true;
        
        % Update lines which pass through target cell
        rc(r1,c1) = s0;
        rs(r1,s1) = c0;
        cs(c1,s1) = r0;
    else
        % Resulting square will be improper
        proper = false;
        
        % Lines which pass through target cell will contain two 1-cells;
        % don't update them (i.e. keep "previous" location of 1-cell) but
        % store the locations of the "extra" 1-cells in auxiliary variables
        r2 = r0;
        c2 = c0;
        s2 = s0;
    end
    
    if np >= NP
        % Sufficient number of proper squares obtained
        break
    end
end
% Maximum number of iterations reached when square was improper;
% restore last proper square
if ~proper
    rc = rcLast;
end