/**
 * A route that displays information about the UW Solar Power Monitor.
 */

import AccountCircleIcon from 'material-ui-icons/AccountCircle';
import Avatar from 'material-ui/Avatar';
import Card, { CardContent, CardHeader } from 'material-ui/Card';
import List, { ListItem, ListItemText } from 'material-ui/List';
import PropTypes from 'prop-types';
import React from 'react';
import Typography from 'material-ui/Typography';

class BuildingsRoute extends React.Component {
  /**
   * Renders the buildings route.
   * @returns {undefined}
   */
  render() {
    return (
      <Card>
        <CardHeader title="About Solar Arrays Located on UW Campus" />
        <CardContent>
          <Typography>There are four solar arrays located on UW Seattle Campus being monitored by UW Solar Monitor project.</Typography>
        </CardContent>
        <CardContent>
          <Typography type="subheading">Buildings</Typography>
          <List>
            <ListItem>
              <ListItemText
                primary="Alder Hall"
                secondary="" />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Elm Hall"
                secondary="" />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Maple Hall"
                secondary="" />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Mercer Court A"
                secondary="" />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    );
  }
}

BuildingsRoute.propTypes = {
};

export default BuildingsRoute;
