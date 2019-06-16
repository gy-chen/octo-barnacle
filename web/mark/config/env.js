const getClientEnvironment = () => {
    return Object.keys(process.env)
        .reduce((env, key) => {
            env[key] = JSON.stringify(process.env[key]);
            return env;
        }, {});
};

module.exports = getClientEnvironment;