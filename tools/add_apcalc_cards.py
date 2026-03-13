import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '11SzrA-74qZgYW9JXpe7LMXb8bDqxSQmL05X6VLYeLcA'
CREDENTIALS_FILE = 'tools/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# 95 AP Calc AB cards
# Columns: id, deck, unit, question, answer, distractor_1, distractor_2, distractor_3,
#          card_type, needs_image, tags, suspended, notes
apcalc_cards = [
    # Unit 1 - Limits and Continuity (suspended=FALSE)
    ['APC-001', 'AP Calculus AB', '1', 'What is the informal definition of a limit?', 'The value a function approaches as the input approaches some value', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-002', 'AP Calculus AB', '1', 'What does \\lim_{x \\to a} f(x) = L mean?', 'As x approaches a, f(x) approaches L', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-003', 'AP Calculus AB', '1', 'What is a one-sided limit?', 'A limit where x approaches a from only one direction (left or right)', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-004', 'AP Calculus AB', '1', 'When does a two-sided limit exist?', 'When the left-hand limit and right-hand limit are both equal', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-005', 'AP Calculus AB', '1', 'What is the limit of a constant function \\lim_{x \\to a} c?', 'c', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-006', 'AP Calculus AB', '1', 'What is the Squeeze Theorem?', 'If g(x) \\leq f(x) \\leq h(x) and \\lim g(x) = \\lim h(x) = L, then \\lim f(x) = L', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits', 'FALSE', ''],
    ['APC-007', 'AP Calculus AB', '1', 'What is \\lim_{x \\to 0} \\frac{\\sin x}{x}?', '1', '', '', '', 'basic', 'TRUE', 'apcalc unit1 limits special', 'FALSE', 'needs graph or unit circle illustration'],
    ['APC-008', 'AP Calculus AB', '1', 'What is \\lim_{x \\to 0} \\frac{1 - \\cos x}{x}?', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits special', 'FALSE', ''],
    ['APC-009', 'AP Calculus AB', '1', 'What does it mean for a function to be continuous at x = a?', '\\lim_{x \\to a} f(x) = f(a), the limit exists, and f(a) is defined', '', '', '', 'basic', 'FALSE', 'apcalc unit1 continuity', 'FALSE', ''],
    ['APC-010', 'AP Calculus AB', '1', 'What are the three conditions for continuity at x = a?', 'f(a) is defined, \\lim_{x \\to a} f(x) exists, and \\lim_{x \\to a} f(x) = f(a)', '', '', '', 'basic', 'FALSE', 'apcalc unit1 continuity', 'FALSE', ''],
    ['APC-011', 'AP Calculus AB', '1', 'What is the Intermediate Value Theorem?', 'If f is continuous on [a,b] and k is between f(a) and f(b), then there exists c in (a,b) with f(c) = k', '', '', '', 'basic', 'FALSE', 'apcalc unit1 continuity ivt', 'FALSE', ''],
    ['APC-012', 'AP Calculus AB', '1', 'What is a vertical asymptote?', 'A vertical line x = a where the function grows without bound as x approaches a', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits asymptotes', 'FALSE', ''],

    # Unit 2 - Differentiation: Definition and Fundamental Properties (suspended=TRUE)
    ['APC-013', 'AP Calculus AB', '2', 'What is the limit definition of the derivative?', "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}", '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives definition', 'TRUE', ''],
    ['APC-014', 'AP Calculus AB', '2', 'What does the derivative represent geometrically?', 'The slope of the tangent line to the curve at that point', '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives', 'TRUE', ''],
    ['APC-015', 'AP Calculus AB', '2', 'What is the Power Rule?', "\\frac{d}{dx} x^n = n x^{n-1}", '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives rules', 'TRUE', ''],
    ['APC-016', 'AP Calculus AB', '2', 'What is the derivative of a constant?', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives rules', 'TRUE', ''],
    ['APC-017', 'AP Calculus AB', '2', 'What is the Sum/Difference Rule for derivatives?', "\\frac{d}{dx}[f(x) \\pm g(x)] = f'(x) \\pm g'(x)", '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives rules', 'TRUE', ''],
    ['APC-018', 'AP Calculus AB', '2', 'What is the Constant Multiple Rule?', "\\frac{d}{dx}[cf(x)] = c f'(x)", '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives rules', 'TRUE', ''],
    ['APC-019', 'AP Calculus AB', '2', 'What is \\frac{d}{dx} \\sin x?', '\\cos x', '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives trig', 'TRUE', ''],
    ['APC-020', 'AP Calculus AB', '2', 'What is \\frac{d}{dx} \\cos x?', '-\\sin x', '', '', '', 'basic', 'TRUE', 'apcalc unit2 derivatives trig', 'TRUE', 'consider sign diagram'],

    # Unit 3 - Differentiation: Composite, Implicit, and Inverse Functions (suspended=TRUE)
    ['APC-021', 'AP Calculus AB', '3', 'What is the Chain Rule?', "\\frac{d}{dx} f(g(x)) = f'(g(x)) \\cdot g'(x)", '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives chain', 'TRUE', ''],
    ['APC-022', 'AP Calculus AB', '3', 'What is the Product Rule?', "\\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)", '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives rules', 'TRUE', ''],
    ['APC-023', 'AP Calculus AB', '3', 'What is the Quotient Rule?', "\\frac{d}{dx}\\left[\\frac{f}{g}\\right] = \\frac{f'g - fg'}{g^2}", '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives rules', 'TRUE', ''],
    ['APC-024', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} e^x?', 'e^x', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives exponential', 'TRUE', ''],
    ['APC-025', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\ln x?', '\\frac{1}{x}', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives logarithmic', 'TRUE', ''],
    ['APC-026', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\tan x?', '\\sec^2 x', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives trig', 'TRUE', ''],
    ['APC-027', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\sec x?', '\\sec x \\tan x', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives trig', 'TRUE', ''],
    ['APC-028', 'AP Calculus AB', '3', 'What is implicit differentiation?', 'Differentiating both sides with respect to x, treating y as a function of x and applying the Chain Rule', '', '', '', 'basic', 'FALSE', 'apcalc unit3 implicit', 'TRUE', ''],
    ['APC-029', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\arcsin x?', '\\frac{1}{\\sqrt{1-x^2}}', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives inverse-trig', 'TRUE', ''],
    ['APC-030', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\arctan x?', '\\frac{1}{1+x^2}', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives inverse-trig', 'TRUE', ''],

    # Unit 4 - Contextual Applications of Differentiation (suspended=TRUE)
    ['APC-031', 'AP Calculus AB', '4', 'What does the first derivative tell us about a function?', 'Whether the function is increasing (positive) or decreasing (negative)', '', '', '', 'basic', 'FALSE', 'apcalc unit4 applications', 'TRUE', ''],
    ['APC-032', 'AP Calculus AB', '4', 'What is the relationship between position, velocity, and acceleration?', "v(t) = s'(t) and a(t) = v'(t) = s''(t)", '', '', '', 'basic', 'FALSE', 'apcalc unit4 motion', 'TRUE', ''],
    ['APC-033', 'AP Calculus AB', '4', "What does it mean when v(t) > 0?", 'The object is moving in the positive direction', '', '', '', 'basic', 'FALSE', 'apcalc unit4 motion', 'TRUE', ''],
    ['APC-034', 'AP Calculus AB', '4', "What does it mean when v(t) < 0?", 'The object is moving in the negative direction', '', '', '', 'basic', 'FALSE', 'apcalc unit4 motion', 'TRUE', ''],
    ['APC-035', 'AP Calculus AB', '4', 'What is a related rates problem?', 'A problem where two or more quantities change with time and their rates of change are related by differentiation', '', '', '', 'basic', 'FALSE', 'apcalc unit4 related-rates', 'TRUE', ''],
    ['APC-036', 'AP Calculus AB', '4', "What is L'Hôpital's Rule?", "If \\lim \\frac{f}{g} gives \\frac{0}{0} or \\frac{\\infty}{\\infty}, then \\lim \\frac{f}{g} = \\lim \\frac{f'}{g'}", '', '', '', 'basic', 'FALSE', "apcalc unit4 lhopital", 'TRUE', ''],
    ['APC-037', 'AP Calculus AB', '4', 'What is a linear approximation?', 'Approximating f(x) near x = a using the tangent line: L(x) = f(a) + f\'(a)(x - a)', '', '', '', 'basic', 'FALSE', 'apcalc unit4 linearization', 'TRUE', ''],

    # Unit 5 - Analytical Applications of Differentiation (suspended=TRUE)
    ['APC-038', 'AP Calculus AB', '5', 'What is the Mean Value Theorem?', "If f is continuous on [a,b] and differentiable on (a,b), then there exists c where f'(c) = \\frac{f(b)-f(a)}{b-a}", '', '', '', 'basic', 'FALSE', 'apcalc unit5 mvt', 'TRUE', ''],
    ['APC-039', 'AP Calculus AB', '5', "What is Rolle's Theorem?", "If f is continuous on [a,b], differentiable on (a,b), and f(a)=f(b), then there exists c in (a,b) where f'(c)=0", '', '', '', 'basic', 'FALSE', 'apcalc unit5 rolles', 'TRUE', ''],
    ['APC-040', 'AP Calculus AB', '5', 'What is a critical point?', "A point where f'(x) = 0 or f'(x) is undefined", '', '', '', 'basic', 'FALSE', 'apcalc unit5 critical-points', 'TRUE', ''],
    ['APC-041', 'AP Calculus AB', '5', 'What is the First Derivative Test?', "If f' changes from positive to negative at c, f has a local max; if negative to positive, a local min", '', '', '', 'basic', 'FALSE', 'apcalc unit5 extrema', 'TRUE', ''],
    ['APC-042', 'AP Calculus AB', '5', 'What is the Second Derivative Test?', "If f'(c)=0 and f''(c)>0, local min; if f''(c)<0, local max; if f''(c)=0, inconclusive", '', '', '', 'basic', 'FALSE', 'apcalc unit5 extrema', 'TRUE', ''],
    ['APC-043', 'AP Calculus AB', '5', 'What does f\'\'(x) > 0 tell us?', 'The function is concave up', '', '', '', 'basic', 'FALSE', 'apcalc unit5 concavity', 'TRUE', ''],
    ['APC-044', 'AP Calculus AB', '5', 'What does f\'\'(x) < 0 tell us?', 'The function is concave down', '', '', '', 'basic', 'FALSE', 'apcalc unit5 concavity', 'TRUE', ''],
    ['APC-045', 'AP Calculus AB', '5', 'What is an inflection point?', "A point where f''(x) changes sign (concavity changes)", '', '', '', 'basic', 'FALSE', 'apcalc unit5 inflection', 'TRUE', ''],
    ['APC-046', 'AP Calculus AB', '5', 'What is an absolute maximum?', 'The largest value of f(x) over its entire domain or a closed interval', '', '', '', 'basic', 'FALSE', 'apcalc unit5 extrema', 'TRUE', ''],
    ['APC-047', 'AP Calculus AB', '5', 'How do you find the absolute extrema on a closed interval [a,b]?', 'Evaluate f at all critical points in (a,b) and at the endpoints a and b; compare all values', '', '', '', 'basic', 'FALSE', 'apcalc unit5 extrema', 'TRUE', ''],

    # Unit 6 - Integration and Accumulation of Change (suspended=TRUE)
    ['APC-048', 'AP Calculus AB', '6', 'What is a definite integral?', 'The net signed area between a function and the x-axis over an interval [a,b]', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration', 'TRUE', ''],
    ['APC-049', 'AP Calculus AB', '6', 'What is an indefinite integral?', 'The general antiderivative of a function: \\int f(x)\\,dx = F(x) + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration', 'TRUE', ''],
    ['APC-050', 'AP Calculus AB', '6', 'What is the Power Rule for integration?', '\\int x^n\\,dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration rules', 'TRUE', ''],
    ['APC-051', 'AP Calculus AB', '6', 'What is \\int e^x\\,dx?', 'e^x + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration exponential', 'TRUE', ''],
    ['APC-052', 'AP Calculus AB', '6', 'What is \\int \\frac{1}{x}\\,dx?', '\\ln|x| + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration logarithmic', 'TRUE', ''],
    ['APC-053', 'AP Calculus AB', '6', 'What is \\int \\cos x\\,dx?', '\\sin x + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration trig', 'TRUE', ''],
    ['APC-054', 'AP Calculus AB', '6', 'What is \\int \\sin x\\,dx?', '-\\cos x + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration trig', 'TRUE', ''],
    ['APC-055', 'AP Calculus AB', '6', 'What is the Fundamental Theorem of Calculus, Part 1?', 'If F(x) = \\int_a^x f(t)\\,dt, then F\'(x) = f(x)', '', '', '', 'basic', 'FALSE', 'apcalc unit6 ftc', 'TRUE', ''],
    ['APC-056', 'AP Calculus AB', '6', 'What is the Fundamental Theorem of Calculus, Part 2?', '\\int_a^b f(x)\\,dx = F(b) - F(a) where F is any antiderivative of f', '', '', '', 'basic', 'FALSE', 'apcalc unit6 ftc', 'TRUE', ''],
    ['APC-057', 'AP Calculus AB', '6', 'What is u-substitution?', 'A technique for integration where u = g(x) and du = g\'(x)dx, transforming the integral', '', '', '', 'basic', 'FALSE', 'apcalc unit6 u-sub', 'TRUE', ''],
    ['APC-058', 'AP Calculus AB', '6', 'What is \\int_a^a f(x)\\,dx?', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration properties', 'TRUE', ''],
    ['APC-059', 'AP Calculus AB', '6', 'What is \\int_a^b f(x)\\,dx + \\int_b^c f(x)\\,dx?', '\\int_a^c f(x)\\,dx', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration properties', 'TRUE', ''],

    # Unit 7 - Differential Equations (suspended=TRUE)
    ['APC-060', 'AP Calculus AB', '7', 'What is a differential equation?', 'An equation relating a function with one or more of its derivatives', '', '', '', 'basic', 'FALSE', 'apcalc unit7 diff-eq', 'TRUE', ''],
    ['APC-061', 'AP Calculus AB', '7', 'What is a slope field?', 'A visual representation of a differential equation showing short line segments with slopes equal to dy/dx at each point', '', '', '', 'basic', 'FALSE', 'apcalc unit7 slope-field', 'TRUE', ''],
    ['APC-062', 'AP Calculus AB', '7', 'What is separation of variables?', 'Rearranging a differential equation so all y terms are on one side and all x terms on the other, then integrating both sides', '', '', '', 'basic', 'FALSE', 'apcalc unit7 separation', 'TRUE', ''],
    ['APC-063', 'AP Calculus AB', '7', 'What is exponential growth/decay model?', '\\frac{dy}{dt} = ky, which has solution y = y_0 e^{kt}', '', '', '', 'basic', 'FALSE', 'apcalc unit7 exponential-model', 'TRUE', ''],
    ['APC-064', 'AP Calculus AB', '7', 'In the model y = y_0 e^{kt}, what does k > 0 indicate?', 'Exponential growth', '', '', '', 'basic', 'FALSE', 'apcalc unit7 exponential-model', 'TRUE', ''],
    ['APC-065', 'AP Calculus AB', '7', 'In the model y = y_0 e^{kt}, what does k < 0 indicate?', 'Exponential decay', '', '', '', 'basic', 'FALSE', 'apcalc unit7 exponential-model', 'TRUE', ''],

    # Unit 8 - Applications of Integration (suspended=TRUE)
    ['APC-066', 'AP Calculus AB', '8', 'How do you find the average value of a function on [a,b]?', '\\frac{1}{b-a} \\int_a^b f(x)\\,dx', '', '', '', 'basic', 'FALSE', 'apcalc unit8 average-value', 'TRUE', ''],
    ['APC-067', 'AP Calculus AB', '8', 'How do you find the area between two curves f(x) and g(x) where f ≥ g on [a,b]?', '\\int_a^b [f(x) - g(x)]\\,dx', '', '', '', 'basic', 'FALSE', 'apcalc unit8 area', 'TRUE', ''],
    ['APC-068', 'AP Calculus AB', '8', 'What is the disk method for volume of revolution around the x-axis?', 'V = \\pi \\int_a^b [f(x)]^2\\,dx', '', '', '', 'basic', 'FALSE', 'apcalc unit8 volume disk', 'TRUE', ''],
    ['APC-069', 'AP Calculus AB', '8', 'What is the washer method for volume of revolution?', 'V = \\pi \\int_a^b \\left([R(x)]^2 - [r(x)]^2\\right)dx where R is outer radius, r is inner radius', '', '', '', 'basic', 'FALSE', 'apcalc unit8 volume washer', 'TRUE', ''],
    ['APC-070', 'AP Calculus AB', '8', 'What is the net change theorem?', '\\int_a^b f\'(x)\\,dx = f(b) - f(a)', '', '', '', 'basic', 'FALSE', 'apcalc unit8 net-change', 'TRUE', ''],
    ['APC-071', 'AP Calculus AB', '8', 'How do you find displacement from a velocity function?', '\\int_{t_1}^{t_2} v(t)\\,dt', '', '', '', 'basic', 'FALSE', 'apcalc unit8 motion', 'TRUE', ''],
    ['APC-072', 'AP Calculus AB', '8', 'How do you find total distance traveled from a velocity function?', '\\int_{t_1}^{t_2} |v(t)|\\,dt', '', '', '', 'basic', 'FALSE', 'apcalc unit8 motion', 'TRUE', ''],
    ['APC-073', 'AP Calculus AB', '8', 'What is the accumulation function?', 'F(x) = \\int_a^x f(t)\\,dt, which accumulates the net area from a to x', '', '', '', 'basic', 'FALSE', 'apcalc unit8 accumulation', 'TRUE', ''],

    # Additional important topics distributed across units
    ['APC-074', 'AP Calculus AB', '2', 'If a function is differentiable at a point, what else must be true?', 'It must be continuous at that point', '', '', '', 'basic', 'FALSE', 'apcalc unit2 continuity differentiability', 'TRUE', ''],
    ['APC-075', 'AP Calculus AB', '2', 'What is the alternate definition of the derivative at x = a?', "f'(a) = \\lim_{x \\to a} \\frac{f(x) - f(a)}{x - a}", '', '', '', 'basic', 'FALSE', 'apcalc unit2 derivatives definition', 'TRUE', ''],
    ['APC-076', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} a^x?', 'a^x \\ln a', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives exponential', 'TRUE', ''],
    ['APC-077', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\log_a x?', '\\frac{1}{x \\ln a}', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives logarithmic', 'TRUE', ''],
    ['APC-078', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\csc x?', '-\\csc x \\cot x', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives trig', 'TRUE', ''],
    ['APC-079', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\cot x?', '-\\csc^2 x', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives trig', 'TRUE', ''],
    ['APC-080', 'AP Calculus AB', '3', 'What is \\frac{d}{dx} \\arccos x?', '-\\frac{1}{\\sqrt{1-x^2}}', '', '', '', 'basic', 'FALSE', 'apcalc unit3 derivatives inverse-trig', 'TRUE', ''],
    ['APC-081', 'AP Calculus AB', '6', 'What is \\int \\sec^2 x\\,dx?', '\\tan x + C', '', '', '', 'basic', 'FALSE', 'apcalc unit6 integration trig', 'TRUE', ''],
    ['APC-082', 'AP Calculus AB', '6', 'What is \\int \\sec x \\tan x\\,dx?', '\\sec x + C', '', '', '', 'basic', 'TRUE', 'apcalc unit6 integration trig', 'TRUE', ''],
    ['APC-083', 'AP Calculus AB', '1', 'What is \\lim_{x \\to \\infty} \\frac{1}{x}?', '0', '', '', '', 'basic', 'FALSE', 'apcalc unit1 limits infinity', 'FALSE', ''],
    ['APC-084', 'AP Calculus AB', '1', 'What is a horizontal asymptote?', 'A horizontal line y = L that the function approaches as x \\to \\pm\\infty', '', '', '', 'basic', 'TRUE', 'apcalc unit1 asymptotes', 'FALSE', ''],
    ['APC-085', 'AP Calculus AB', '5', 'What does the graph of f\' tell us about f?', "Where f' > 0, f is increasing; where f' < 0, f is decreasing; where f' = 0, possible extremum", '', '', '', 'basic', 'TRUE', 'apcalc unit5 curve-sketching', 'TRUE', ''],
    ['APC-086', 'AP Calculus AB', '5', 'What does the graph of f\'\' tell us about f?', "Where f'' > 0, f is concave up; where f'' < 0, f is concave down; sign change means inflection point", '', '', '', 'basic', 'TRUE', 'apcalc unit5 curve-sketching', 'TRUE', ''],
    ['APC-087', 'AP Calculus AB', '6', 'What is a Riemann sum?', 'An approximation of a definite integral using rectangles: \\sum_{i=1}^n f(x_i^*)\\Delta x', '', '', '', 'basic', 'TRUE', 'apcalc unit6 riemann', 'TRUE', ''],
    ['APC-088', 'AP Calculus AB', '6', 'What is the left Riemann sum?', 'Uses the left endpoint of each subinterval as the sample point', '', '', '', 'basic', 'FALSE', 'apcalc unit6 riemann', 'TRUE', ''],
    ['APC-089', 'AP Calculus AB', '6', 'What is the right Riemann sum?', 'Uses the right endpoint of each subinterval as the sample point', '', '', '', 'basic', 'FALSE', 'apcalc unit6 riemann', 'TRUE', ''],
    ['APC-090', 'AP Calculus AB', '6', 'What is the midpoint Riemann sum?', 'Uses the midpoint of each subinterval as the sample point', '', '', '', 'basic', 'FALSE', 'apcalc unit6 riemann', 'TRUE', ''],
    ['APC-091', 'AP Calculus AB', '8', 'What is the cross-section method for volume?', 'V = \\int_a^b A(x)\\,dx where A(x) is the area of the cross-section at x', '', '', '', 'basic', 'TRUE', 'apcalc unit8 volume cross-section', 'TRUE', ''],
    ['APC-092', 'AP Calculus AB', '8', 'How do you set up a volume integral using vertical slices?', 'Integrate with respect to x: V = \\int_a^b A(x)\\,dx', '', '', '', 'basic', 'TRUE', 'apcalc unit8 volume', 'TRUE', ''],
    ['APC-093', 'AP Calculus AB', '4', 'What is the equation of the tangent line to f at x = a?', "y = f(a) + f'(a)(x - a)", '', '', '', 'basic', 'FALSE', 'apcalc unit4 tangent-line', 'TRUE', ''],
    ['APC-094', 'AP Calculus AB', '7', 'What is Euler\'s method?', "A numerical method to approximate solutions to dy/dx = f(x,y) using y_{n+1} = y_n + f(x_n, y_n)\\Delta x", '', '', '', 'basic', 'FALSE', 'apcalc unit7 eulers-method', 'TRUE', ''],
    ['APC-095', 'AP Calculus AB', '2', 'What notation can be used for the derivative?', "f'(x), \\frac{dy}{dx}, \\frac{d}{dx}f(x), and y' are all equivalent", '', '', '', 'basic', 'FALSE', 'apcalc unit2 notation', 'TRUE', ''],
]

print(f"Total AP Calc cards to add: {len(apcalc_cards)}")

# Step 1: Append cards to cards_master
print("Appending cards to cards_master...")
result = sheet.values().append(
    spreadsheetId=SPREADSHEET_ID,
    range='cards_master!A:M',
    valueInputOption='RAW',
    insertDataOption='INSERT_ROWS',
    body={'values': apcalc_cards}
).execute()
print(f"  Added {result['updates']['updatedRows']} rows")

# Step 2: Fix anki tab formulas
# Current anki tab: 111 rows (1 header + 110 data)
# After append: 111 + 95 = 206 rows total in cards_master
# Anki tab needs formulas for rows 2-206
# The correct formula uses D (question, col 4) and E (answer, col 5)

print("Rebuilding anki tab formulas...")

# Build all formula rows
anki_rows = []

# Row 1: header references (keep as-is, A1/B1/D1 for id/deck/question header)
anki_rows.append(['=cards_master!A1', '=cards_master!B1', '=cards_master!D1'])

# Rows 2-206: data formulas (D=question, E=answer)
for i in range(2, 207):
    formula = f'="\\("&cards_master!D{i}&"\\) = {{{{c1::\\("&cards_master!E{i}&"\\)}}}}"'
    anki_rows.append([
        f'=cards_master!A{i}',
        f'=cards_master!B{i}',
        formula
    ])

# Clear anki tab first
sheet.values().clear(
    spreadsheetId=SPREADSHEET_ID,
    range='anki!A:C'
).execute()
print("  Cleared old anki tab")

# Write new formulas
sheet.values().update(
    spreadsheetId=SPREADSHEET_ID,
    range='anki!A1',
    valueInputOption='USER_ENTERED',
    body={'values': anki_rows}
).execute()
print(f"  Wrote {len(anki_rows)} formula rows to anki tab")

print("\nDone! cards_master now has 111 + 95 = 206 data rows.")
print("Anki tab formulas now correctly reference columns D (question) and E (answer).")