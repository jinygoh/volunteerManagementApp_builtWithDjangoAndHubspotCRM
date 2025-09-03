const jwt = require('jsonwebtoken');

module.exports = function (req, res, next) {
  // Get token from header
  const authHeader = req.header('Authorization');

  // Check if not token
  if (!authHeader) {
    return res.status(401).json({ msg: 'No token, authorization denied' });
  }

  // Check if the token is in the correct 'Bearer <token>' format
  const token = authHeader.split(' ')[1];
  if (!token) {
    return res.status(401).json({ msg: 'Token format is invalid, authorization denied' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Add user from payload
    req.user = decoded.user;
    next();
  } catch (err) {
    res.status(401).json({ msg: 'Token is not valid' });
  }
};
